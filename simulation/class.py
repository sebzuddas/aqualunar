import pandas as pd
import matplotlib.pyplot as plt

class Stock:
    def __init__(self, name: str, initial_value: float = 0, limit:float = None) -> None:
        self.name = name
        self.value = initial_value
        self.limit = limit

    def update(self, change: float) -> None:
        print(f"Updating {self.name}: Current Value={self.value}, Change={change}")  # Debug print
        if self.limit is not None and (self.value + change) > self.limit:
            print(f"Limit reached for {self.name}. Limit={self.limit}")  # Debug print
            self.value = self.limit
        else:
            self.value = max(self.value + change, 0)
        print(f"After Update {self.name}: New Value={self.value}")  # Debug print


class Flow:
    def __init__(self, name: str, source=None, destination=None, rate_function=None) -> None:
        self.name = name
        if name == source:
            self.source = None
        else:
            self.source = source
        self.destination = destination
        # rate_function is a function that defines how the flow rate is calculated
        self.rate_function = rate_function

    def execute(self) -> None:
        if self.rate_function is not None:
            flow_rate = self.rate_function()
            # print(f"Executing flow {self.name} with rate {flow_rate}")  # Diagnostic print
            if self.source is not None:
                # print(f"Before source update: {self.source.value}")  # Diagnostic print
                self.source.update(-flow_rate)
                # print(f"After source update: {self.source.value}")  # Diagnostic print
            if self.destination is not None:
                # print(f"Before destination update: {self.destination.value}")  # Diagnostic print
                self.destination.update(flow_rate)
                # print(f"After destination update: {self.destination.value}")  # Diagnostic print
        else:
            raise RuntimeError(f"Please input a rate function for the stock: {self.name}")


class System:
    def __init__(self, t: int, stocks=None, flows=None) -> None:
        """
        Defines the whole system. Input the number of timesteps 't' you want to simulate,
        along with optional lists of Stock and Flow objects to initialize the system.
        """
        self.stocks = stocks if stocks is not None else []  # Initialize stocks as a list
        self.flows = flows if flows is not None else []  # Initialize flows as a list
        self.history = []  # To store the history of stock values
        self.t = t

    def add_stock(self, stock: Stock) -> None:
        self.stocks.append(stock)

    def add_flow(self, flow: Flow) -> None:
        self.flows.append(flow)

    def step(self) -> None:
        # Execute each flow
        for flow in self.flows:
            flow.execute()
        
        current_stock_values = {stock.name: stock.value for stock in self.stocks}
        self.history.append(current_stock_values)

    def simulate(self) -> None:
        for _ in range(self.t):
            self.step()

    def print_history(self) -> None:
        for step, data in enumerate(self.history):
            print(f"Step {step}: {data}")

    def show(self):
        plt.figure(figsize=(10, 6))
        for stock_name in self.history[0].keys():  # Assume all histories have the same keys
            plt.plot([step[stock_name] for step in self.history], label=stock_name)
        plt.title("Stock Values Over Time")
        plt.xlabel("Time Step")
        plt.ylabel("Stock Value")
        plt.legend()
        plt.show()
    


# Example usage
if __name__ == "__main__":
    #get the elements sheet 
    elements = pd.read_excel('Aqualunar_map.xlsx', sheet_name='Elements')
    # print(elements)
    connections = pd.read_excel('Aqualunar_map.xlsx', sheet_name='Connections')
    # print(connections.to_string())
    
    # get the stocks from the elements sheet and create an object from each one
    stocks = elements.loc[elements['Type']=='Stock']
    # print(stocks)
    # stock_list = [Stock(row['Label'], 1, limit=2000) for index, row in stocks.iterrows()]


    # Step 1: Create a dictionary mapping stock names to Stock objects
    stock_dict = {row['Label']: Stock(row['Label'], 1, limit=2000) for index, row in stocks.iterrows()}

    # Step 2: Create Flow objects, using the stock_dict to reference the correct Stock objects
    # flows_list = [Flow(row['Label'], row['From']=stock_dict, row['To']=stock_dict, lambda: 1) for index, row in connections.iterrows()]

    flows_list = [
        Flow(
            name=row['Label'],
            source=None if row['From'] == row['Label'] else stock_dict.get(row['From']),
            destination=stock_dict.get(row['To']),
            rate_function=lambda: 6  # Adjust the rate function as necessary
        ) 
        for index, row in connections.iterrows()
    ]
    
    # # print([flow.name for flow in flows_list])
    # print([flow.source for flow in flows_list])
    # print([flow.destination for flow in flows_list])
    # exit()
    # print([source.destination = for source in sources_list])


    # Setup system
    aqualunar_system = System(t=10, stocks=list(stock_dict.values()), flows=flows_list)

    # for stock, flow in zip(stock_list, flows_list):
    #     aqualunar_system.add_stock(stock)
    #     aqualunar_system.add_flow(flow)

    # Simulate a step
    aqualunar_system.simulate()
    aqualunar_system.show()
    # water_system.show()
    print(aqualunar_system.history)