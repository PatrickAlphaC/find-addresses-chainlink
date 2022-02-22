from brownie import network, Contract, interface, config, multicall
import json


def get_aggregators():
    file = open("data.json")
    data = json.load(file)
    eth_proxy_addresses = []
    aggregator_addresses = []
    total_number_addresses = 0
    print("Getting addresses for network:")
    print(network.show_active())
    for blockchain in data:
        for networks in data[blockchain]["networks"]:
            if networks["name"] == config["networks"][network.show_active()]["label"]:
                for proxy in networks["proxies"]:
                    total_number_addresses = total_number_addresses + 1
                    eth_proxy_addresses.append(proxy["proxy"])
    print(
        f"There are {total_number_addresses} price feeds on network {network.show_active()}"
    )
    multicall(address=config["networks"][network.show_active()]["multicall2"])
    print("Doing multicall...")
    with multicall:
        for proxy in eth_proxy_addresses:
            price_feed = Contract.from_abi(
                "feed",
                proxy,
                interface.AggregatorV3Interface.abi,
            )
            aggregator_address = price_feed.aggregator()
            aggregator_addresses.append(str(aggregator_address))
    print("Printing...")
    with open(f"./results/{network.show_active()}-result.json", "w") as outfile:
        json.dump(aggregator_addresses, outfile)


def main():
    get_aggregators()
