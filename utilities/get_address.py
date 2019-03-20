from juujian import verify, find_index


def get_address(info: list):
    # The address starts after the website and stops before one of these six lines.
    phone = [line for line in info if len(line) >= 3 and line[3] == '-' and line[7] == '-']
    email = [line for line in info if '@' in line]
    tasting = [line for line in info if line.startswith('Tasting')]
    cases = [line for line in info if line.startswith('Cases:')]
    regions = [line for line in info if line.startswith('Regions:')]
    founded = [line for line in info if line.startswith('Founded:')]

    phone = verify(phone)
    email = verify(email)
    tasting = verify(tasting)
    cases = verify(cases)
    regions = verify(regions)
    founded = verify(founded)

    phone_index = find_index(phone, info)
    email_index = find_index(email, info)
    tasting_index = find_index(tasting, info)
    cases_index = find_index(cases, info)
    regions_index = find_index(regions, info)
    founded_index = find_index(founded, info)

    # We know that for any entry in the website, the address ends with the first of whichever of the above
    # information is available. Therefore, if we take the min of their indexes, we will find the confines of the
    # address.
    stop_line = min(phone_index, email_index, tasting_index, cases_index, regions_index, founded_index)

    address = info[2:stop_line]
    return address
