class BarcodeReader:
    def __init__(self, device_path='/dev/hidraw0'):
        self.device_path = device_path
        self.hid = {
            4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 
            11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 
            17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 
            23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 
            29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 
            35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 
            45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 
            52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'
        }

        self.hid2 = {
            4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 
            11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 
            23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 
            35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 
            52: '"', 53: '~', 54: '<', 55: '>', 56: '?'
        }

    def read_barcode(self):
        try:
            with open(self.device_path, 'rb') as fp:
                ss = ""
                shift = False
                done = False

                while not done:
                    buffer = fp.read(8)  # Read 8 bytes from the HID device
                    
                    for byte in buffer:
                        if byte > 0:  # Check if the byte is greater than 0
                            if byte == 40:  # Carriage return
                                done = True
                                break

                            if shift:
                                if byte == 2:  # Shift key
                                    shift = True
                                else:
                                    ss += self.hid2.get(byte, '')  # Use get to avoid KeyError
                                    shift = False
                            else:
                                if byte == 2:  # Shift key
                                    shift = True
                                else:
                                    ss += self.hid.get(byte, '')  # Use get to avoid KeyError
                return ss
            
        except IOError as e:
            print(f"Error reading from HID device: {e}")
            return ""

# Example of how to use the BarcodeReader class
if __name__ == '__main__':
    barcode_reader = BarcodeReader()
    
    try:
        while True:
            output = barcode_reader.read_barcode()
            if output:  # Only print if there is output
                print(output)
    except KeyboardInterrupt:
        pass
