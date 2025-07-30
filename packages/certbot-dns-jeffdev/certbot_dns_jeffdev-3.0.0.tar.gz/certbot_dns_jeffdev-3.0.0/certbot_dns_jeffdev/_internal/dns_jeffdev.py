"""DNS Authenticator for jeffdev DNS."""
import logging
from typing import Any
from typing import Callable
from typing import Tuple
from typing import Optional

import requests

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Jeffdev DNS

    This Authenticator uses the Jeffdev DNS API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using jeffdev DNS api for DNS)."
    ttl = 120

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(
        cls, add: Callable[..., None], default_propagation_seconds: int = 120
    ) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="Jeffdev DNS credentials INI file.")

    def more_info(self) -> str:
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge using the Jeffdev DNS API."

    def _validate_credentials(self, credentials: CredentialsConfiguration) -> None:
        key = credentials.conf("api-key")
        if not key:
            raise errors.PluginError(
                "{}: api-key required for authentication".format(
                    credentials.confobj.filename
                )
            )

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "Jeffdev DNS credentials INI file",
            None,
            self._validate_credentials,
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_jeffdev_client().add_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_jeffdev_client().del_txt_record(domain, validation_name, validation)

    def _get_jeffdev_client(self) -> "_JeffdevDnsClient":
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return _JeffdevDnsClient(self.credentials.conf("api-key"))


class _JeffdevDnsClient:
    """
    Encapsulates all communication with the Jeffdev DNS API.
    """

    def __init__(self, api_key: str) -> None:
        self.headers = {"Accept": "application/json", "X-Api-Key": api_key}

    def add_txt_record(
        self, domain: str, record_name: str, record_content: str, record_ttl: int
    ) -> None:
        """
        Add a TXT record using the supplied information.

        :param str domain: The domain to use to look up the JeffDev DNS zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the Jeffdev DNS API
        """

        zone_name = self._find_zone(domain)

        # Set content type because we are posting
        post_headers = self.headers
        post_headers["Content-Type"] = "application/json"

        # Check if record_name contains zone_name (it should) and remove it
        if record_name.endswith(zone_name):
            record_name = record_name[: -(len(zone_name) + 1)]

        payload = {
            "Type": "TXT",
            "Ttl": record_ttl,
            "Name": record_name,
            "Value": record_content,
        }

        response = requests.put(
            f"https://dns-api.jeffdev.nl/api/v1/zone/{zone_name}/records",
            json=payload,
            headers=post_headers,
        )
        logger.debug("Attempting to add record to zone %s: %s", zone_name, payload)

        # make sure that jeffdev dns api responded with code 201
        if response.status_code != 200:
            raise errors.PluginError(
                f"API error ({response.status_code}): {response.text}"
            )

        record_id = self._find_txt_record_id(zone_name, record_name, record_content)
        logger.debug("Successfully added TXT record with record_id: %s", record_id)

    def del_txt_record(
        self, domain: str, record_name: str, record_content: str
    ) -> None:
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain: The domain to use to look up the Jeffdev DNS zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """

        try:
            zone_name = self._find_zone(domain)
        except errors.PluginError as e:
            logger.debug("Encountered error finding zone_id during deletion: %s", e)
            return

        # Check if record_name contains zone_name (it should) and remove it
        if record_name.endswith(zone_name):
            record_name = record_name[: -(len(zone_name) + 1)]

        if zone_name:
            record_id = self._find_txt_record_id(zone_name, record_name, record_content)
            if record_id:
                response = requests.delete(
                    f"https://dns-api.jeffdev.nl/api/v1/zone/{zone_name}/records/{record_id}",
                    headers=self.headers,
                )
                # make sure that jeffdev api responded with code 201
                if response.status_code != 200:
                    logger.error(
                        "API error (%s): %s", response.status_code, response.text
                    )
            else:
                logger.debug("TXT record not found; no cleanup needed.")
        else:
            logger.debug("Zone not found; no cleanup needed.")

    def _find_zone(self, domain: str) -> str:
        """
        Find the zone_id for a given domain.

        :param str domain: The domain for which to find the zone_id.
        :returns: The zone_id and zone_name, if found.
        :rtype: tuple(str, str)
        :raises certbot.errors.PluginError: if no zone_id is found.
        """

        zone_name_guesses = dns_common.base_domain_name_guesses(domain)

        # Note: this request may not contain the zone if there are more than 1000 zones!
        dnszone_request = requests.get(
            "https://dns-api.jeffdev.nl/api/v1/zone", headers=self.headers
        )

        # make sure that jeffdev dns api responded with code 200
        if dnszone_request.status_code != 200:
            raise errors.PluginError(
                f"API error ({dnszone_request.status_code}): {dnszone_request.text}"
            )

        dnszones = dnszone_request.json()
        # Iterate through zones and find the first one that's in our list of guesses (earlier guesses are more specific)
        for zone_name_guess in zone_name_guesses:
            for dnszone in dnszones["data"]:
                if dnszone["name"] == zone_name_guess:
                    logger.debug(
                        "Found %s using name %s",
                        domain,
                        dnszone["name"],
                    )
                    return zone_name_guess
        raise errors.PluginError("Could not find zone in account.")

    def _find_txt_record_id(
        self, zone_name: str, record_name: str, record_content: str
    ) -> Optional[str]:
        """
        Find the record_id for a TXT record with the given name and content.

        :param str zone_id: The zone_id which contains the record.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :returns: The record_id, if found.
        :rtype: str
        """

        dnszone_request = requests.get(
            f"https://dns-api.jeffdev.nl/api/v1/zone/{zone_name}", headers=self.headers
        )

        # make sure that jeffdev dns api responded with code 200
        if dnszone_request.status_code != 200:
            raise errors.PluginError(
                f"API error ({dnszone_request.status_code}): {dnszone_request.text}"
            )

        dnsrecords = dnszone_request.json()
        # Iterate through records and find a TXT record (type 3) with the right name and value
        for dnsrecord in dnsrecords["data"]["records"]:
            if (
                dnsrecord["type"] == "TXT"
                and dnsrecord["name"] == record_name
                and dnsrecord["value"] == record_content
            ):
                record_id = dnsrecord["id"]
                return record_id
        logger.debug("Unable to find TXT record.")
        return None
