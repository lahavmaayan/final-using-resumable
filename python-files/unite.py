import sys

def unite(file):
    i = 1
    final = open(file + ".JSON", "a")
    while (i > 0):
        try:
            f = open(file + "." + str(i), "r")
            print "[+] Writing part " + str(i)
            lines = f.read()
            final.write(lines)
            i += 1
            f.close()
        except:
            print "[+] Done"
            i = 0
            final.close()

def main():
    unite(sys.argv[1])

if __name__ == "__main__":
    main()
