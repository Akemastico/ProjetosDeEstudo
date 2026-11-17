from graph import buildGraph


started = {}
started["board"] = ["1"] * 9


if __name__ == "__main__":
    result = buildGraph().invoke({"board" : ["."]  * 9})