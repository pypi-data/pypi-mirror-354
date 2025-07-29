def show_functions():
    print("\n📘 Excel Utility Library - Function Showcase\n")

    functions = [
        {
            "name": "create_excel(file_path, columns)",
            "desc": "Create a new Excel file with specified column headers.",
            "example": 'create_excel("data.xlsx", ["Name", "Date", "In", "Out", "Total"])'
        },
        {
            "name": "append_row(file_path, data)",
            "desc": "Append a dictionary as a new row to the Excel file.",
            "example": 'append_row("data.xlsx", {"Name": "Alice", "Date": "2025-06-10", "In": "09:00", "Out": "17:00", "Total": "8:00"})'
        },
        {
            "name": "read_excel(file_path)",
            "desc": "Read and return Excel content as a DataFrame.",
            "example": 'df = read_excel("data.xlsx")'
        },
        {
            "name": "filter_rows(file_path, column, value)",
            "desc": "Return rows where the given column equals the specified value.",
            "example": 'df = filter_rows("data.xlsx", "Name", "Alice")'
        },
        {
            "name": "update_cell(file_path, row_index, column_name, new_value)",
            "desc": "Update a specific cell by row index and column name.",
            "example": 'update_cell("data.xlsx", 0, "Total", "8:15")'
        },
        {
            "name": "delete_row(file_path, row_index)",
            "desc": "Delete a row by its index.",
            "example": 'delete_row("data.xlsx", 0)'
        },
        {
            "name": "get_row_count(file_path)",
            "desc": "Return the number of rows in the Excel file (excluding header).",
            "example": 'count = get_row_count("data.xlsx")'
        },
        {
            "name": "get_column_names(file_path)",
            "desc": "Return a list of column names.",
            "example": 'columns = get_column_names("data.xlsx")'
        },
        {
            "name": "sort_by_column(file_path, column, ascending=True)",
            "desc": "Sort the Excel file by a column and save the result.",
            "example": 'sort_by_column("data.xlsx", "Name")'
        },
        {
            "name": "rename_column(file_path, old_name, new_name)",
            "desc": "Rename a column in the Excel file.",
            "example": 'rename_column("data.xlsx", "Name", "FullName")'
        },
        {
            "name": "clear_excel(file_path, keep_header=True)",
            "desc": "Clear all data (optionally keep headers).",
            "example": 'clear_excel("data.xlsx")'
        },
        {
            "name": "get_unique_values(file_path, column)",
            "desc": "Return unique values from a column.",
            "example": 'unique = get_unique_values("data.xlsx", "Name")'
        },
        {
            "name": "column_stats(file_path, column)",
            "desc": "Return min, max, mean, median for a numeric column.",
            "example": 'stats = column_stats("data.xlsx", "TotalHours")'
        }
    ]

    for fn in functions:
        print(f"🔹 {fn['name']}")
        print(f"   → {fn['desc']}")
        print(f"   ⤷ Example: {fn['example']}\n")

if __name__ == "__main__":
    show_functions()
