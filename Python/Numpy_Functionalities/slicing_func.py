class SimpleArray:
    def __init__(self, data):
        self.data = data

    def get(self, row, col):
        """Get the element at the specified row and column."""
        return self.data[row][col]

    def set(self, row, col, value):
        """Set the element at the specified row and column."""
        self.data[row][col] = value

    def slice(self, row_slice, col_slice):
        """Get a subarray using slicing for rows and columns."""
        sliced_data = [row[col_slice] for row in self.data[row_slice]]
        return SimpleArray(sliced_data)

    def __repr__(self):
        """String representation of the array."""
        return "\n".join(str(row) for row in self.data)


# Example usage
if __name__ == "__main__":
    # Create a 2D array
    array = SimpleArray([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    print("Original Array:")
    print(array)

    # Access an element
    print("\nElement at (1, 2):", array.get(1, 2))  # Output: 6

    # Modify an element
    array.set(1, 2, 99)
    print("\nModified Array:")
    print(array)

    # Slice the array
    sliced_array = array.slice(slice(0, 2), slice(1, 3))  # Rows 0-1, Columns 1-2
    print("\nSliced Array (Rows 0-1, Columns 1-2):")
    print(sliced_array)