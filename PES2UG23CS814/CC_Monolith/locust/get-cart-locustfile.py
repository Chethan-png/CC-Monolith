from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login


class AddToCart(FastHttpUser):
    def on_start(self):
        self.username = "PES2UG23CS814"
        self.password = "Chethan@2"
        cookies = login(self.username, self.password)
        if not cookies:
            raise Exception("Login failed: Unable to retrieve cookies or token")
        self.token = cookies.get("token")

    host = "http://localhost:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def view_cart(self):
        response = self.client.get(
            "/cart",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                "Cookie": f"token={self.token}",
                "Host": "localhost:5000",
                "Priority": "u=0, i",
                "Referer": "http://localhost:5000/product/1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            },
            name="View /cart"
        )
        if response.status_code != 200:
            response.failure(f"Failed to load /cart: {response.status_code}")


if __name__ == "__main__":
    run_single_user(AddToCart)
