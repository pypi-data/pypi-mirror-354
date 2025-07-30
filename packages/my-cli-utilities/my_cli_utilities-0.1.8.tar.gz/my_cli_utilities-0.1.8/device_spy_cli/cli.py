# -*- coding: utf-8 -*-

import json
import fire
from typing import Optional, Dict, List, Any
from my_cli_utilities_common.http_helpers import make_sync_request
from my_cli_utilities_common.pagination import paginated_display
from my_cli_utilities_common.config import BaseConfig, LoggingUtils

# Initialize logger
logger = LoggingUtils.setup_logger('device_spy_cli')

# Configuration constants
class Config(BaseConfig):
    BASE_URL = "https://device-spy-mthor.int.rclabenv.com"
    HOSTS_ENDPOINT = f"{BASE_URL}/api/v1/hosts"
    ALL_DEVICES_ENDPOINT = f"{BASE_URL}/api/v1/hosts/get_all_devices"
    LABELS_ENDPOINT = f"{BASE_URL}/api/v1/labels/"
    DEVICE_ASSETS_ENDPOINT = f"{BASE_URL}/api/v1/device_assets/"


class DeviceSpyCli:
    """
    A CLI tool to interact with the Device Spy service.
    Provides commands to query device information, available devices, and host details.
    """

    @staticmethod
    def _print_json(data: Any, title: str = "") -> None:
        """Print JSON data with optional title."""
        if title:
            print(f"\n{title}")
        print(json.dumps(data, indent=2, ensure_ascii=False))



    def _display_device_info(self, device: Dict) -> None:
        """Display device information in a user-friendly format."""
        print(f"\n📱 Device Information")
        print("=" * Config.DISPLAY_WIDTH)
        
        # Extract key information
        udid = device.get("udid", "N/A")
        platform = device.get("platform", "N/A")
        model = device.get("model", "N/A")
        os_version = device.get("platform_version", "N/A")  # API returns platform_version
        hostname = device.get("hostname", "N/A")
        host_ip = device.get("host_ip", "N/A")  # Original IP address
        location = device.get("location", "N/A")
        is_locked = device.get("is_locked", False)
        ip_port = device.get("ip_port", "N/A")
        
        print(f"📋 UDID:           {udid}")
        print(f"🔧 Platform:       {platform}")
        print(f"📟 Model:          {model}")
        print(f"🎯 OS Version:     {os_version}")
        print(f"🖥️  Host:           {hostname}")
        if host_ip != "N/A":
            print(f"🌐 Host IP:        {host_ip}")
        if location != "N/A":
            print(f"📍 Location:       {location}")
        if ip_port != "N/A":
            print(f"🌐 IP:Port:        {ip_port}")
        
        status = "🔒 Locked" if is_locked else "✅ Available"
        print(f"🔐 Status:         {status}")
        
        print("=" * Config.DISPLAY_WIDTH)

    def _get_device_location_from_assets(self, udid: str) -> Optional[str]:
        """Fetch device location from assets by UDID."""
        response_data = make_sync_request(Config.DEVICE_ASSETS_ENDPOINT)
        if response_data:
            device_assets = response_data.get("data", [])
            for device_asset in device_assets:
                if device_asset.get("udid") == udid:
                    location = device_asset.get("location")
                    return location
        return None

    def _get_host_alias(self, host_ip: str) -> Optional[str]:
        """Fetch host alias by IP address."""
        response_data = make_sync_request(Config.HOSTS_ENDPOINT)
        if response_data:
            hosts = response_data.get("data", [])
            for host in hosts:
                if host.get("hostname") == host_ip:
                    alias = host.get("alias")
                    return alias
        return None

    def udid(self, udid: str) -> None:
        """Display detailed information for a specific device.

        Args:
            udid: The Unique Device Identifier (UDID) of the device to query.
        """
        print(f"\n🔍 Looking up device information...")
        print(f"   UDID: {udid}")
        
        response_data = make_sync_request(Config.ALL_DEVICES_ENDPOINT)
        if not response_data:
            print(f"   ❌ Failed to fetch device data from API")
            return

        devices = response_data.get("data", [])
        for device_data in devices:
            if udid == device_data.get("udid"):
                print(f"   ✅ Device found")
                
                # Prepare device info
                device_info = device_data.copy()
                original_hostname = device_info.get("hostname")

                # Get host alias and preserve original IP
                host_alias = self._get_host_alias(original_hostname)
                if host_alias:
                    device_info["hostname"] = host_alias
                    device_info["host_ip"] = original_hostname  # Preserve original IP

                # Add IP:Port for Android devices
                if device_info.get("platform") == "android":
                    adb_port = device_info.get("adb_port")
                    if adb_port:
                        device_info["ip_port"] = f"{original_hostname}:{adb_port}"

                # Get location information
                location = self._get_device_location_from_assets(udid)
                if location:
                    device_info["location"] = location

                # Clean up unnecessary fields
                keys_to_delete = ["is_simulator", "remote_control", "adb_port"]
                for key in keys_to_delete:
                    if key in device_info:
                        del device_info[key]

                # Display formatted device info
                self._display_device_info(device_info)
                return
        
        print(f"   ❌ Device with UDID '{udid}' not found")

    def available_devices(self, platform: str) -> None:
        """List available (not locked, not simulator) devices for a platform.

        Args:
            platform: The platform to filter by (e.g., "android", "ios").
        """
        print(f"\n🔍 Finding available devices...")
        print(f"   Platform: {platform}")
        
        response_data = make_sync_request(Config.ALL_DEVICES_ENDPOINT)
        if not response_data:
            print(f"   ❌ Failed to fetch device data from API")
            return

        all_devices = response_data.get("data", [])
        available_devices = []

        for device in all_devices:
            if (
                not device.get("is_locked")
                and not device.get("is_simulator")
                and device.get("platform") == platform
            ):
                available_devices.append(device)

        print(f"   ✅ Found {len(available_devices)} available {platform} devices")
        
        if available_devices:
            # Define the display function for each device
            def display_device(device: Dict, index: int) -> None:
                udid = device.get("udid", "N/A")
                model = device.get("model", "N/A")
                os_version = device.get("platform_version", "N/A")  # API returns platform_version
                hostname = device.get("hostname", "N/A")
                
                print(f"\n{index}. {model} ({os_version})")
                print(f"   UDID: {udid}")
                print(f"   Host: {hostname}")
            
            # Use paginated display
            title = f"📱 Available {platform.capitalize()} Devices"
            completed = paginated_display(
                available_devices, 
                display_device, 
                title, 
                Config.PAGE_SIZE, 
                Config.DISPLAY_WIDTH
            )
            
            # Show footer information
            print("\n" + "=" * Config.DISPLAY_WIDTH)
            print(f"💡 Use 'ds info <udid>' to get detailed information")
            print("=" * Config.DISPLAY_WIDTH)
        else:
            print(f"\n   ℹ️  No available {platform} devices found")

    def get_host_ip(self, query_string) -> None:
        """Find host IP address(es) based on a query string.

        The query string is matched against host information fields like alias or hostname.

        Args:
            query_string: The string to search for within host information.
        """
        # Convert to string to handle cases where Fire passes numeric values
        query_str = str(query_string)
        
        # Handle special case: when user inputs .XXX, Fire converts it to 0.XXX
        # We want to convert it back to .XXX for IP suffix matching
        if query_str.startswith('0.') and len(query_str.split('.')) == 2:
            # Check if the part after decimal is all digits
            decimal_part = query_str.split('.')[1]
            if decimal_part.isdigit():
                query_str = '.' + decimal_part
                print(f"\n🔍 Searching for hosts...")
                print(f"   Query: '{query_str}' (IP suffix search)")
            else:
                print(f"\n🔍 Searching for hosts...")
                print(f"   Query: '{query_str}'")
        else:
            print(f"\n🔍 Searching for hosts...")
            print(f"   Query: '{query_str}'")
        
        response_data = make_sync_request(Config.HOSTS_ENDPOINT)
        if not response_data:
            print(f"   ❌ Failed to fetch host data from API")
            return

        hosts = response_data.get("data", [])
        found_hosts = []
        
        for host in hosts:
            matched_fields = []
            for key, value in host.items():
                if query_str.lower() in str(value).lower():
                    matched_fields.append(key)
            
            if matched_fields:
                # Add matched fields info to host data
                host_with_match_info = host.copy()
                host_with_match_info['_matched_fields'] = matched_fields
                found_hosts.append(host_with_match_info)

        if not found_hosts:
            print(f"   ❌ No host found matching '{query_str}'")
        elif len(found_hosts) == 1:
            host = found_hosts[0]
            hostname = host.get("hostname", "N/A")
            alias = host.get("alias", "N/A")
            matched_fields = host.get("_matched_fields", [])
            print(f"   ✅ Found single host: {hostname}")
            
            print(f"\n🖥️  Host Information")
            print("=" * Config.DISPLAY_WIDTH)
            print(f"🌐 IP Address:     {hostname}")
            if alias != "N/A":
                print(f"🏷️  Alias:          {alias}")
            
            # Show matched fields
            if matched_fields:
                matched_display = ", ".join(matched_fields)
                print(f"🔍 Matched in:     {matched_display}")
            
            print("=" * Config.DISPLAY_WIDTH)
        else:
            # Check if all hosts match the same field(s)
            all_matched_fields = [set(host.get("_matched_fields", [])) for host in found_hosts]
            common_fields = set.intersection(*all_matched_fields) if all_matched_fields else set()
            
            if common_fields and len(all_matched_fields) > 1:
                # All hosts match the same field(s) - show it in the search summary
                if len(common_fields) == 1:
                    field_name = list(common_fields)[0]
                    print(f"   Matched: {field_name}")
                    print(f"   ✅ Found {len(found_hosts)} matching hosts")
                    show_individual_matches = False
                else:
                    field_names = ", ".join(sorted(common_fields))
                    print(f"   Matched: {field_names}")
                    print(f"   ✅ Found {len(found_hosts)} matching hosts")
                    show_individual_matches = False
            else:
                print(f"   ✅ Found {len(found_hosts)} matching hosts")
                show_individual_matches = True
            
            print(f"\n🖥️  Matching Hosts")
            print("=" * Config.DISPLAY_WIDTH)
            
            for i, host in enumerate(found_hosts, 1):
                hostname = host.get("hostname", "N/A")
                alias = host.get("alias", "N/A")
                matched_fields = host.get("_matched_fields", [])
                print(f"\n{i}. {hostname}")
                if alias != "N/A":
                    print(f"   Alias: {alias}")
                
                # Show matched fields only if different hosts match different fields
                if show_individual_matches and matched_fields:
                    matched_display = ", ".join(matched_fields)
                    print(f"   Matched: {matched_display}")
            
            print("\n" + "=" * Config.DISPLAY_WIDTH)

    # Short aliases for convenience
    def devices(self, platform: str) -> None:
        """Short alias for available_devices. List available devices for a platform."""
        self.available_devices(platform)

    def host(self, query_string) -> None:
        """Short alias for get_host_ip. Find host IP by query string."""
        self.get_host_ip(query_string)

    def help(self) -> None:
        """Display available commands and their descriptions."""
        header_color = "\033[95m"
        bold = "\033[1m"
        end = "\033[0m"
        
        print(f"{header_color}Device Spy CLI Commands{end}")
        print("\nAvailable commands:")
        print(f"  {bold}info <udid>{end}                        - Get detailed device information")
        print(f"  {bold}available_devices <platform>{end}       - List available devices (android/ios)")
        print(f"    {bold}devices <platform>{end}               - Short alias")
        print(f"  {bold}get_host_ip <query>{end}                - Find host IP address by query")
        print(f"    {bold}host <query>{end}                     - Short alias")
        print(f"  {bold}help{end}                               - Show this help")
        
        print(f"\nExamples:")
        print(f"  {bold}ds info A1B2C3D4E5F6{end}              - Get info for specific device")
        print(f"  {bold}ds devices android{end}                - List available Android devices")
        print(f"  {bold}ds devices ios{end}                    - List available iOS devices")
        print(f"  {bold}ds host lab{end}                       - Find hosts containing 'lab'")
        print(f"  {bold}ds host 192.168{end}                   - Find hosts with IP containing '192.168'")
        print(f"  {bold}ds host .201{end}                      - Find hosts with IP ending in '.201'")
        print(f"  {bold}ds host XMNA067{end}                   - Find host by alias name")
        print(f"  {bold}ds host 15.4{end}                      - Find hosts with macOS version 15.4")


def main_ds_function():
    fire.Fire(DeviceSpyCli)


if __name__ == "__main__":
    main_ds_function()
