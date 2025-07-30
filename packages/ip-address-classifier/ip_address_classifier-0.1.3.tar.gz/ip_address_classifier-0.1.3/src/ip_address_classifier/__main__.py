def main():
    # Program instructions:
    print('This program accepts an IPv4 address and tells you:'
    '\n- it\'s class (A, B, C, D, E)'
    '\n- if it is public or private'
    '\n- if it is invalid'
    '\n- if it is a loopback'
    )

    # User input:
    print('\n\nInput a valid IPv4 address int he form of X.X.X.X,\nwhere each x is an integer from 0 to 255.\nFor example 192.168.1.1')
    ipv4 = input('\nEnter address here: ')

    # Split method from module 4 instructions on canvas:
    my_octet_list = ipv4.split('.')

    # Check that there are exactly 4 octets
    if len(my_octet_list) != 4:
        print(f'\n{ipv4} is an invalid address (must have 4 octets).')
        return

    # List comprehension from module 4 instructions on canvas:
    try:
        my_octet_list = [int(i) for i in my_octet_list]
    except ValueError:
        print(f'\n{ipv4} is an invalid address (contains non-integer values).')
        return

    print(f'\nThe entered address, {ipv4}, has been split into a list: {my_octet_list}')

    # Invalid addresses:
    if my_octet_list[0] == 0:
        ipv4_class = 'invalid'
        print(f'\n{ipv4} is an {ipv4_class} address.')
    elif my_octet_list[0] > 255 or my_octet_list[1] > 255 or my_octet_list[2] > 255 or my_octet_list[3] > 255:
        ipv4_class = 'invalid'
        print(f'\n{ipv4} is a {ipv4_class} address.')

    # Routable addresses:
    else:
        if my_octet_list[0] != 0:
        # ---------Class A adress--------
            if my_octet_list[0] < 128:
                ipv4_class = 'class A'
                if my_octet_list[0] == 10:
                    scope = 'private address'
                elif my_octet_list[0] == 127:
                    scope = 'loopback address'
                else:
                    scope = 'public address'
        # ---------Class B adress--------
            elif my_octet_list[0] < 192:
                ipv4_class = 'class B'
                if my_octet_list[0] == 172 and (16 <= my_octet_list[1] <= 31):
                    scope = 'private address'
                else: 
                    scope = 'public address'
        # ---------Class C adress--------
            elif my_octet_list[0] < 224:
                ipv4_class = 'class C'
                if my_octet_list[0] == 192 and my_octet_list[1] == 168:
                    scope = 'private address'
                else:
                    scope = 'public address'
        # ---------Class D adress--------
            elif my_octet_list[0] < 240:
                ipv4_class = 'class D multicast'
                scope = 'address'
        # ---------Class E adress--------
            elif my_octet_list[0] <= 255:
                ipv4_class = 'class E experimental'
                scope = 'address'
        print(f'\n{ipv4} is a {ipv4_class} {scope}.')
