class Resource:
    def __init__(self, resource: dict[str, int]) -> None:
        self.data = resource

    def get_report(self) -> None:
        """Prints the current available quantity of each resource."""
        report=frozendict()

    def check_sufficient_resources(self, sandwich_ingredients:dict[str, int]) -> bool:
       
        for item, required_amount in sandwich_ingredients.items():
            if self.data.get(item, 0) < required_amount:
                print(f"Sorry, there is not enough {item}.")
                return False
        return True

    def remove_resources(self, sandwich_ingredients: dict[str, int]) -> None:
        """Deducts the used ingredients from the inventory after making a sandwich."""
        for item, required_amount in sandwich_ingredients.items():
            self.data[item] -= required_amount