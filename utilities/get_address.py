from juujian import verify, find_index


def get_address(info: list):
    # The address starts after the website and stops before one of these six lines.
    phone = [line for line in info if len(line) >= 8 and line[3] == '-' and line[7] == '-']
    email = [line for line in info if '@' in line]
    tasting = [line for line in info if line.startswith('Tasting')]
    tasting2 = [line for line in info if line.startswith('See tasting')]
    cases = [line for line in info if line.startswith('Cases:')]
    regions = [line for line in info if line.startswith('Regions:')]
    founded = [line for line in info if line.startswith('Founded:')]
    review = [line for line in info if 'Review' in line]

    phone = verify(phone)
    email = verify(email)
    tasting = verify(tasting)
    tasting2 = verify(tasting2)
    cases = verify(cases)
    regions = verify(regions)
    founded = verify(founded)
    review = verify(review)

    phone_index = find_index(phone, info)
    email_index = find_index(email, info)
    tasting_index = find_index(tasting, info)
    tasting2_index = find_index(tasting2, info)
    cases_index = find_index(cases, info)
    regions_index = find_index(regions, info)
    founded_index = find_index(founded, info)

    # We know that for any entry in the website, the address ends with the first of whichever of the above
    # information is available. Therefore, if we take the min of their indexes, we will find the confines of the
    # address.
    stop_line = min(phone_index, email_index, tasting_index, tasting2_index, cases_index, regions_index, founded_index)

    # If there is a line with review in the info, we need to start two lines after that line.
    if review:
        review_line = info.index(review)
        address = info[(review_line + 2):stop_line]
    elif len(info) > 3 and info[2].startswith('www.'):
        address = info[3:stop_line]
    else:
        address = info[2:stop_line]

    if len(address) >= 2:
        address = '\n'.join(address)
    elif isinstance(address, list) and len(address) == 1:
        address = address[0]
    return address
