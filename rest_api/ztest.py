import requests as rq

def main():
    urls = ["https://api.github.com/repos/gcc-mirror/gcc"]
    resp = []

    for u in urls:
        currResp = rq.get(u)
        resp.append(currResp.json())

    print(resp)

if __name__ == "__main__":
    main()
