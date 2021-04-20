def parse_destination_coordinates(dest_coordinates):
    dest_coordinates = [str(elem).replace(".", "") for elem in dest_coordinates]
    return dest_coordinates


def parse_coordinates(coordinates):
    for i in range(len(coordinates)):
        if len(coordinates[i]) > 8:
            coordinates[i] = coordinates[i][:8]
        else:
            for j in range(8 - len(coordinates[i])):
                coordinates[i] += "0"
    coordinates = [int(elem) for elem in coordinates]
    return coordinates
