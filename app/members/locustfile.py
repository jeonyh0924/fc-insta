from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.get("/users")
        self.client.patch("/users/1", headers={'Authorization': 'token 806ba2900ca6c3f4579c1fe11b2f9115d50213f4'})
        self.client.get('/posts', headers={'Authorization': 'token 079be089ea946e240b928942b2b333e9ec41432d'})
        self.client.patch('/posts/1', headers={'Authorization': 'token c72f979a81308e7e376037c197ed570a1c359f8c'})
        self.client.patch('/posts/1', headers={'Authorization': 'token 4fdc2998402eb1fc824f425984509bdab48dccf5'})

    @task(2)
    def cycle(self):
        self.client.post("/users/login", {"email": "admin@admin.com", "password": "1111"})
        self.client.get('/users/1', headers={'Authorization': 'token c72f979a81308e7e376037c197ed570a1c359f8c'})
        self.client.delete('/users/logout', headers={'Authorization': 'token c72f979a81308e7e376037c197ed570a1c359f8c'})

    # @task(3)
    # def view_item(self):
    #     item_id = random.randint(1, 10000)
    #     self.client.get(f"/item?id={item_id}", name="/item")

    def on_start(self):
        self.client.post("/users/login", {"email": "admin@admin.com", "password": "1111"})
        self.client.post("/users/login", {"email": "admin11@admin.com", "password": "1111"})
        data = {
            "email": "admin@admin.com",
            "password": "1111"
        }
