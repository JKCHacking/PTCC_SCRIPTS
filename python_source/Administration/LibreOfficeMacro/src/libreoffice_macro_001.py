def CountLocator(data_range, compare_range):
    compare_str = "".join(str(x).strip() for x in compare_range[0])
    count = 0
    located_row = []
    for i, row in enumerate(data_range):
        row_str = "".join(str(x).strip() for x in row)
        if row_str == compare_str:
            count += 1
            located_row.append("Row {}".format(str(i + 1)))
    if count == 1:
        duplicate_string = "No Duplicates"
    else:
        duplicate_string = ", ".join(located_row)
    output_string = "Count: {}, Located Duplicates: {}".format(count, duplicate_string)
    return output_string


g_exportedScripts = (CountLocator,)
