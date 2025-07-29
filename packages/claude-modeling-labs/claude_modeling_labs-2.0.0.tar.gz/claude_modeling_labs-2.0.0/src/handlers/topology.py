"""
Topology Handler

Handles node creation, interface management, and link creation in CML labs.
"""

import sys
from typing import Dict, Any, Union, Optional, List
from fastmcp import FastMCP

from ..client import get_client
from ..utils import check_auth, handle_api_error


def register_topology_tools(mcp: FastMCP):
    """Register topology management tools with the MCP server"""
    
    @mcp.tool()
    async def get_lab_nodes(lab_id: str) -> Union[Dict[str, Any], str]:
        """
        Get all nodes in a specific lab
        
        Args:
            lab_id: ID of the lab
        
        Returns:
            Dictionary of nodes in the lab or error message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/nodes")
            nodes = response.json()
            
            # If the response is a list, convert it to a dictionary
            if isinstance(nodes, list):
                print(f"Converting nodes list to dictionary", file=sys.stderr)
                result = {}
                for node in nodes:
                    node_id = node.get("id")
                    if node_id:
                        result[node_id] = node
                return result
            
            return nodes
        except Exception as e:
            return f"Error getting lab nodes: {str(e)}"

    @mcp.tool()
    async def add_node(
        lab_id: str, 
        label: str, 
        node_definition: str, 
        x: int = 0, 
        y: int = 0,
        populate_interfaces: bool = True,
        ram: Optional[int] = None,
        cpu_limit: Optional[int] = None,
        parameters: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Add a node to the specified lab
        
        Args:
            lab_id: ID of the lab
            label: Label for the new node
            node_definition: Type of node (e.g., 'iosv', 'csr1000v')
            x: X coordinate for node placement
            y: Y coordinate for node placement
            populate_interfaces: Whether to automatically create interfaces
            ram: RAM allocation for the node (optional)
            cpu_limit: CPU limit for the node (optional)
            parameters: Node-specific parameters (optional)
        
        Returns:
            Dictionary with node ID and confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            # Construct the node data payload
            node_data = {
                "label": label,
                "node_definition": node_definition,
                "x": x,
                "y": y,
                "parameters": parameters or {},
                "tags": [],
                "hide_links": False
            }
            
            # Add optional parameters if provided
            if ram is not None:
                node_data["ram"] = ram
            
            if cpu_limit is not None:
                node_data["cpu_limit"] = cpu_limit
            
            # Add populate_interfaces as a query parameter if needed
            endpoint = f"/api/v0/labs/{lab_id}/nodes"
            if populate_interfaces:
                endpoint += "?populate_interfaces=true"
            
            # Make the API request with explicit Content-Type header
            headers = {"Content-Type": "application/json"}
            response = await get_client().request(
                "POST",
                endpoint,
                json=node_data,
                headers=headers
            )
            
            # Process the response
            result = response.json()
            node_id = result.get("id")
            
            if not node_id:
                return {"error": "Failed to create node, no node ID returned", "response": result}
            
            return {
                "node_id": node_id,
                "message": f"Added node '{label}' with ID: {node_id}",
                "status": "success",
                "details": result
            }
        except Exception as e:
            return handle_api_error("add_node", e)

    @mcp.tool()
    async def create_router(
        lab_id: str,
        label: str,
        x: int = 0,
        y: int = 0
    ) -> Dict[str, Any]:
        """
        Create a router with the 'iosv' node definition
        
        Args:
            lab_id: ID of the lab
            label: Label for the new router
            x: X coordinate for node placement
            y: Y coordinate for node placement
        
        Returns:
            Dictionary with node ID and confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        # Use add_node with the router node definition
        return await add_node(lab_id, label, "iosv", x, y, True)

    @mcp.tool()
    async def create_switch(
        lab_id: str,
        label: str,
        x: int = 0,
        y: int = 0
    ) -> Dict[str, Any]:
        """
        Create a switch with the 'iosvl2' node definition
        
        Args:
            lab_id: ID of the lab
            label: Label for the new switch
            x: X coordinate for node placement
            y: Y coordinate for node placement
        
        Returns:
            Dictionary with node ID and confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        # Use add_node with the switch node definition
        return await add_node(lab_id, label, "iosvl2", x, y, True)

    @mcp.tool()
    async def get_node_interfaces(lab_id: str, node_id: str) -> Union[Dict[str, Any], str, List[str]]:
        """
        Get interfaces for a specific node
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
        
        Returns:
            Dictionary of node interfaces or error message or list of interface IDs
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/nodes/{node_id}/interfaces")
            interfaces = response.json()
            
            # Check if the response is a list of interface IDs
            if isinstance(interfaces, list):
                print(f"Got list of interface IDs: {interfaces}", file=sys.stderr)
                return interfaces
            elif isinstance(interfaces, str):
                # If it's a string, it might be a concatenated list of UUIDs
                print(f"Got string of interface IDs: {interfaces}", file=sys.stderr)
                # Parse as UUIDs (36 characters per UUID)
                if len(interfaces) % 36 == 0:
                    return [interfaces[i:i+36] for i in range(0, len(interfaces), 36)]
                else:
                    return interfaces
            else:
                # If it's a dictionary, return it as is
                return interfaces
        except Exception as e:
            print(f"Error getting node interfaces: {str(e)}", file=sys.stderr)
            return f"Error getting node interfaces: {str(e)}"

    @mcp.tool()
    async def get_physical_interfaces(lab_id: str, node_id: str) -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        """
        Get all physical interfaces for a specific node
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
        
        Returns:
            List of physical interfaces or error message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            # First get all interfaces
            interfaces_response = await get_node_interfaces(lab_id, node_id)
            
            # Handle different return types
            interface_ids = []
            if isinstance(interfaces_response, str) and "Error" in interfaces_response:
                return interfaces_response
            elif isinstance(interfaces_response, list):
                interface_ids = interfaces_response
            elif isinstance(interfaces_response, str):
                # Parse as UUIDs if needed
                if len(interfaces_response) % 36 == 0:
                    interface_ids = [interfaces_response[i:i+36] for i in range(0, len(interfaces_response), 36)]
                else:
                    return f"Unexpected interface response format: {interfaces_response}"
            elif isinstance(interfaces_response, dict):
                interface_ids = list(interfaces_response.keys())
            else:
                return f"Unexpected interface response type: {type(interfaces_response)}"
            
            # Get details for each interface and filter for physical interfaces
            physical_interfaces = []
            for interface_id in interface_ids:
                interface_details = await get_client().request("GET", f"/api/v0/labs/{lab_id}/interfaces/{interface_id}")
                interface_data = interface_details.json()
                
                # Check if it's a physical interface
                is_physical = interface_data.get("type") == "physical"
                
                # If type is not present, check other attributes that might indicate a physical interface
                if "type" not in interface_data:
                    # Most physical interfaces have a slot number
                    if "slot" in interface_data:
                        is_physical = True
                
                if is_physical:
                    physical_interfaces.append(interface_data)
            
            if not physical_interfaces:
                return f"No physical interfaces found for node {node_id}"
            
            return physical_interfaces
        except Exception as e:
            return handle_api_error("get_physical_interfaces", e)

    @mcp.tool()
    async def create_interface(lab_id: str, node_id: str, slot: int = 4) -> Dict[str, Any]:
        """
        Create an interface on a node
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
            slot: Slot number for the interface (default: 4)
        
        Returns:
            Dictionary with interface ID and confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            # Import here to avoid circular imports
            from .lab_management import get_lab_details
            
            # Check if the lab is running
            lab_details = await get_lab_details(lab_id)
            if isinstance(lab_details, dict) and lab_details.get("state") == "STARTED":
                return {"error": "Cannot create interfaces while the lab is running. Please stop the lab first."}
            
            print(f"Creating interface on node {node_id}, slot {slot}", file=sys.stderr)
            
            # Construct the proper payload format
            interface_data = {
                "node": node_id,
                "slot": slot
            }
            
            print(f"Interface creation payload: {interface_data}", file=sys.stderr)
            
            # Make the API request
            response = await get_client().request(
                "POST", 
                f"/api/v0/labs/{lab_id}/interfaces",
                json=interface_data
            )
            
            # Process the response
            result = response.json()
            print(f"Interface creation response: {result}", file=sys.stderr)
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                # Sometimes the API returns a list of created interfaces
                interface_id = result[0].get("id")
                interface_label = result[0].get("label")
                return {
                    "interface_id": interface_id,
                    "message": f"Created interface {interface_label} on node {node_id}, slot {slot}",
                    "status": "success",
                    "details": result
                }
            elif isinstance(result, dict):
                # Sometimes it returns a single object
                interface_id = result.get("id")
                interface_label = result.get("label")
                if interface_id:
                    return {
                        "interface_id": interface_id,
                        "message": f"Created interface {interface_label} on node {node_id}, slot {slot}",
                        "status": "success",
                        "details": result
                    }
            
            return {"error": "Failed to create interface, unexpected response format", "response": result}
        except Exception as e:
            return handle_api_error("create_interface", e)

    @mcp.tool()
    async def get_lab_links(lab_id: str) -> Union[Dict[str, Any], str]:
        """
        Get all links in a specific lab
        
        Args:
            lab_id: ID of the lab
        
        Returns:
            Dictionary of links in the lab or error message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/links")
            links = response.json()
            
            # If the response is a list, convert it to a dictionary
            if isinstance(links, list):
                print(f"Converting links list to dictionary", file=sys.stderr)
                result = {}
                for link in links:
                    link_id = link.get("id")
                    if link_id:
                        result[link_id] = link
                return result
            
            return links
        except Exception as e:
            return f"Error getting lab links: {str(e)}"

    @mcp.tool()
    async def create_link_v3(lab_id: str, interface_id_a: str, interface_id_b: str) -> Dict[str, Any]:
        """
        Create a link between two interfaces in a lab (alternative format)
        
        Args:
            lab_id: ID of the lab
            interface_id_a: ID of the first interface
            interface_id_b: ID of the second interface
        
        Returns:
            Dictionary with link ID and confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            print(f"Creating link between interfaces {interface_id_a} and {interface_id_b}", file=sys.stderr)
            
            # Try the standard format with src_int and dst_int
            link_data = {
                "src_int": interface_id_a,
                "dst_int": interface_id_b
            }
            
            headers = {"Content-Type": "application/json"}
            response = await get_client().request(
                "POST", 
                f"/api/v0/labs/{lab_id}/links",
                json=link_data,
                headers=headers
            )
            
            result = response.json()
            print(f"Link creation response: {result}", file=sys.stderr)
            
            # Extract the link ID from the response
            link_id = result.get("id")
            if not link_id:
                return {"error": "Failed to create link, no link ID returned", "response": result}
            
            return {
                "link_id": link_id,
                "message": f"Created link between interfaces {interface_id_a} and {interface_id_b}",
                "status": "success",
                "details": result
            }
        except Exception as e:
            # If the first format failed, try an alternative format
            try:
                print("First format failed, trying alternative format...", file=sys.stderr)
                link_data_alt = {
                    "i1": interface_id_a,
                    "i2": interface_id_b
                }
                
                response_alt = await get_client().request(
                    "POST", 
                    f"/api/v0/labs/{lab_id}/links",
                    json=link_data_alt,
                    headers=headers
                )
                
                result_alt = response_alt.json()
                print(f"Link creation response (alt format): {result_alt}", file=sys.stderr)
                
                link_id_alt = result_alt.get("id")
                if link_id_alt:
                    return {
                        "link_id": link_id_alt,
                        "message": f"Created link between interfaces {interface_id_a} and {interface_id_b} using alternative format",
                        "status": "success",
                        "details": result_alt
                    }
                
                return {"error": "Failed to create link with both formats"}
            except Exception as alt_err:
                print(f"Alternative format also failed: {str(alt_err)}", file=sys.stderr)
                return handle_api_error("create_link", e)

    async def find_available_interface(lab_id: str, node_id: str) -> Union[str, Dict[str, str]]:
        """
        Find an available physical interface on a node
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
            
        Returns:
            Interface ID or error dictionary
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            # Get interfaces for the node with operational=true to get details
            interfaces_response = await get_client().request(
                "GET", 
                f"/api/v0/labs/{lab_id}/nodes/{node_id}/interfaces?operational=true"
            )
            interfaces = interfaces_response.json()
            
            # Ensure we have an array of interfaces
            if isinstance(interfaces, str):
                interfaces = interfaces.split()
            elif isinstance(interfaces, dict):
                interfaces = list(interfaces.keys())
            
            # Make sure we have interfaces to work with
            if not interfaces:
                return {"error": f"No interfaces found for node {node_id}"}
            
            # Find first available physical interface
            for interface_id in interfaces:
                # Get detailed info for this interface
                interface_detail = await get_client().request(
                    "GET", 
                    f"/api/v0/labs/{lab_id}/interfaces/{interface_id}?operational=true"
                )
                interface_data = interface_detail.json()
                
                # Check if physical and not connected
                if (interface_data.get("type") == "physical" and 
                    interface_data.get("is_connected") == False):
                    return interface_id
            
            return {"error": f"No available physical interface found for node {node_id}"}
        except Exception as e:
            return handle_api_error("find_available_interface", e)

    @mcp.tool()
    async def link_nodes(lab_id: str, node_id_a: str, node_id_b: str) -> Dict[str, Any]:
        """
        Create a link between two nodes by automatically selecting appropriate interfaces
        
        Args:
            lab_id: ID of the lab
            node_id_a: ID of the first node
            node_id_b: ID of the second node
        
        Returns:
            Dictionary with link ID and confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            # Find available interfaces on both nodes
            interface_a = await find_available_interface(lab_id, node_id_a)
            if isinstance(interface_a, dict) and "error" in interface_a:
                return interface_a
            
            interface_b = await find_available_interface(lab_id, node_id_b)
            if isinstance(interface_b, dict) and "error" in interface_b:
                return interface_b
            
            # Create the link using these interfaces
            return await create_link_v3(lab_id, interface_a, interface_b)
        except Exception as e:
            return handle_api_error("link_nodes", e)

    @mcp.tool()
    async def delete_link(lab_id: str, link_id: str) -> str:
        """
        Delete a link from a lab
        
        Args:
            lab_id: ID of the lab
            link_id: ID of the link to delete
        
        Returns:
            Confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            response = await get_client().request("DELETE", f"/api/v0/labs/{lab_id}/links/{link_id}")
            return f"Link {link_id} deleted successfully"
        except Exception as e:
            return f"Error deleting link: {str(e)}"

    @mcp.tool()
    async def get_lab_topology(lab_id: str) -> str:
        """
        Get a detailed summary of the lab topology
        
        Args:
            lab_id: ID of the lab
        
        Returns:
            Formatted summary of the lab topology
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            # Import here to avoid circular imports
            from .lab_management import get_lab_details
            
            # Get lab details
            lab_details = await get_lab_details(lab_id)
            if isinstance(lab_details, dict) and "error" in lab_details:
                return lab_details["error"]
            
            # Get nodes
            nodes = await get_lab_nodes(lab_id)
            if isinstance(nodes, str) and "Error" in nodes:
                return nodes
            
            # Get links
            links = await get_lab_links(lab_id)
            if isinstance(links, str) and "Error" in links:
                return links
            
            # Create a topology summary
            result = f"Lab Topology: {lab_details.get('title', 'Untitled')}\n"
            result += f"State: {lab_details.get('state', 'unknown')}\n"
            result += f"Description: {lab_details.get('description', 'None')}\n\n"
            
            # Add nodes
            result += "Nodes:\n"
            for node_id, node in nodes.items():
                result += f"- {node.get('label', 'Unnamed')} (ID: {node_id})\n"
                result += f"  Type: {node.get('node_definition', 'unknown')}\n"
                result += f"  State: {node.get('state', 'unknown')}\n"
            
            # Add links
            result += "\nLinks:\n"
            for link_id, link in links.items():
                src_node_id = link.get('src_node')
                dst_node_id = link.get('dst_node')
                
                if src_node_id in nodes and dst_node_id in nodes:
                    src_node = nodes[src_node_id].get('label', src_node_id)
                    dst_node = nodes[dst_node_id].get('label', dst_node_id)
                    result += (f"- Link {link_id}: {src_node} ({link.get('src_int', 'unknown')}) → "
                               f"{dst_node} ({link.get('dst_int', 'unknown')})\n")
                else:
                    result += f"- Link {link_id}: {src_node_id}:{link.get('src_int')} → {dst_node_id}:{link.get('dst_int')}\n"
            
            return result
        except Exception as e:
            return f"Error getting lab topology: {str(e)}"
