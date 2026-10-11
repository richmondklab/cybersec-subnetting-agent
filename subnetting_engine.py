import ipaddress
import random


def cidr_to_mask(cidr: int) -> str:
    """Convert CIDR prefix length to a dotted decimal mask."""
    if not 0 <= cidr <= 32:
        raise ValueError("CIDR must be between 0 and 32.")

    if cidr == 0:
        return "0.0.0.0"

    mask_value = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
    return ".".join(str((mask_value >> shift) & 0xFF) for shift in (24, 16, 8, 0))


def mask_to_cidr(mask: str) -> int:
    """Convert dotted-decimal mask to CIDR prefix length."""
    try:
        ip = ipaddress.IPv4Address(mask)
    except ipaddress.AddressValueError as exc:
        raise ValueError(f"Invalid subnet mask: {mask}") from exc

    binary = "".join(f"{byte:08b}" for byte in ip.packed)
    first_zero_index = binary.find("0")
    if first_zero_index == -1:
        return 32
    return first_zero_index


def calculate_network(ip: str, cidr: int = None, mask: str = None) -> dict:
    """Calculate network information for a given IP and mask/CIDR."""
    if cidr is None:
        if mask is None:
            raise ValueError("You must provide either CIDR or subnet mask.")
        cidr = mask_to_cidr(mask)

    if not 0 <= cidr <= 32:
        raise ValueError("CIDR must be between 0 and 32.")

    network = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)
    hosts = list(network.hosts())

    first_host = str(hosts[0]) if hosts else "N/A"
    last_host = str(hosts[-1]) if hosts else "N/A"
    usable_hosts = max(network.num_addresses - 2, 0)

    return {
        "ip": ip,
        "cidr": cidr,
        "subnet_mask": str(network.netmask),
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "first_host": first_host,
        "last_host": last_host,
        "total_addresses": network.num_addresses,
        "usable_hosts": usable_hosts,
        "wildcard_mask": str(network.hostmask),
        "host_range": f"{first_host} - {last_host}",
    }


def generate_exercise(exercise_type: str = "basic") -> dict:
    """Generate a network lab exercise."""
    examples = [
        ("192.168.10.0", 26),
        ("10.0.0.0", 24),
        ("172.16.0.0", 20),
        ("192.168.1.0", 30),
        ("10.10.10.0", 29),
    ]

    ip, cidr = random.choice(examples)

    if exercise_type == "vlsm":
        prompt = "Design subnets for HR (50 hosts), IT (25 hosts), and Sales (100 hosts) inside 10.0.0.0/24."
        return {
            "exercise_type": "vlsm",
            "prompt": prompt,
            "network": "10.0.0.0/24",
            "requirements": {
                "HR": 50,
                "IT": 25,
                "Sales": 100,
            },
        }

    prompt = f"Calculate the subnet details for {ip}/{cidr}. Show the network address, broadcast address, subnet mask, first host, last host, and usable host count."
    return {
        "exercise_type": "basic",
        "prompt": prompt,
        "ip": ip,
        "cidr": cidr,
    }


def get_fallback_hint(exercise: dict, step: int = 1) -> str:
    """Return a safe, built-in hint for the user."""
    if exercise.get("exercise_type") == "vlsm":
        hints = {
            1: "Start by determining the largest required subnet and assign it first.",
            2: "Use the number of hosts to choose the smallest subnet that can fit each department.",
            3: "Remember to avoid overlap and keep each subnet contiguous.",
        }
        return hints.get(step, "Check each department's host requirement against the subnet size before assigning it.")

    ip = exercise.get("ip")
    cidr = exercise.get("cidr")
    hints = {
        1: "First, convert the subnet mask from CIDR notation. This tells you how many bits are used for the network portion.",
        2: "The network address is the first address in the range and the broadcast address is the last address in the range.",
        3: f"For {ip}/{cidr}, calculate the range carefully and subtract 2 addresses for the network and broadcast when counting usable hosts.",
        4: "Double-check that the first host is one greater than the network address and the last host is one less than the broadcast address.",
    }
    return hints.get(step, "Recalculate the host range and verify the network and broadcast addresses before answering.")


def explain_concept(concept: str) -> str:
    """Explain a networking concept in simple terms."""
    concept_lower = concept.lower()

    if "subnet mask" in concept_lower or "subnetting" in concept_lower:
        return (
            "Subnetting divides one large network into smaller logical subnetworks. "
            "The subnet mask tells you which bits are network bits and which bits are host bits. "
            "A shorter subnet mask gives you more host addresses, while a longer subnet mask creates smaller subnets."
        )

    if "cidr" in concept_lower:
        return (
            "CIDR, or Classless Inter-Domain Routing, represents the network prefix with a slash notation such as /24. "
            "The number after the slash tells you how many bits are reserved for the network portion."
        )

    if "broadcast" in concept_lower:
        return (
            "The broadcast address is the last address in a subnet. It is used to send data to all devices in that subnet at once. "
            "Hosts cannot normally use the broadcast address as a unique host address."
        )

    if "network address" in concept_lower:
        return (
            "The network address is the first address of a subnet. It identifies the subnet itself and is not assigned to a host. "
            "It is the base address for that network segment."
        )

    return (
        f"The concept '{concept}' is important in network design because it helps reduce address waste, improve routing, and control traffic in smaller segments. "
        "Think of it as a way to divide a larger IP range into smaller, organized groups."
    )


def normalize_answer(answer: dict) -> dict:
    """Normalize commonly used answer keys to the engine's expected format."""
    normalized = {}
    if not isinstance(answer, dict):
        return normalized

    field_map = {
        "network": "network_address",
        "network_address": "network_address",
        "broadcast": "broadcast_address",
        "broadcast_address": "broadcast_address",
        "mask": "subnet_mask",
        "subnet_mask": "subnet_mask",
        "first": "first_host",
        "first_host": "first_host",
        "last": "last_host",
        "last_host": "last_host",
        "usable": "usable_hosts",
        "usable_hosts": "usable_hosts",
    }

    for key, value in answer.items():
        normalized[field_map.get(key.lower(), key)] = value

    return normalized


def check_answer(exercise: dict, user_answer: dict) -> dict:
    """Grade a student's subnetting answer."""
    expected = {} 
    if exercise.get("exercise_type") == "vlsm":
        return {
            "score": 100,
            "passed": True,
            "feedback": "VLSM exercises are design tasks. Check that your subnets are contiguous, non-overlapping, and large enough for each department.",
            "expected": "Design a valid VLSM plan for the required departments",
        }

    ip = exercise.get("ip")
    cidr = exercise.get("cidr")
    expected = calculate_network(ip, cidr=cidr)
    answer = normalize_answer(user_answer)

    required_fields = [
        "network_address",
        "broadcast_address",
        "subnet_mask",
        "first_host",
        "last_host",
        "usable_hosts",
    ]

    score = 0
    feedback = []

    for field in required_fields:
        expected_value = expected.get(field)
        actual_value = answer.get(field)

        if actual_value == expected_value:
            score += 16
            feedback.append(f"{field}: correct")
        else:
            feedback.append(f"{field}: expected {expected_value}, got {actual_value}")

    total_score = max(0, min(100, score))
    return {
        "score": total_score,
        "passed": total_score >= 80,
        "feedback": "\n".join(feedback),
        "expected": expected,
    }
