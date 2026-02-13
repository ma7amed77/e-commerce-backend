
def test_adding_user_good(client):
    response = client.post("/auth/register", 
                           json={
                               "name":'Mohamed',
                               "email":'mohamed@gamil.com',
                               "password":'12345678'
                               })
    assert response.status_code == 200

def test_adding_user_bad(client, auth_token):
    response = client.post("/auth/register", 
                           json={
                               "name":'Mohamed',
                               "email":auth_token["email"],
                               "password":'12345678'
                               })
    assert response.status_code == 409
    response = client.post("/auth/register", 
                           json={
                               "name":'Mohamed',
                               "email":'mohamed2@gmail',
                               "password":'12345678'
                               })
    assert response.status_code == 422
    response = client.post("/auth/register", 
                           json={
                               "name":'Mohamed',
                               "email":'mohamed3@gamil.com',
                               "password":'12348'
                               })
    assert response.status_code == 422

def test_seller(client, auth_token):
    response = client.post(
        "/seller/new",
        headers={"auth":auth_token["token"]},
        json={"name":"Mohamed's Shop"}
    )
    assert response.status_code == 200
    seller_Token = response.json()['access_token']
    assert seller_Token

def test_seller_login(client, seller_token):
    email = seller_token["email"]
    response = client.post(
        "/auth/login",
        json={"email":email, "password":'12345678'}
    )
    assert response.status_code == 200
    user_token = response.json()["access_token"]
    response = client.post(
        "/seller",
        headers={"auth":user_token}
    )
    assert response.status_code == 200
    seller_Token = response.json()['access_token']
    assert seller_Token

# More tests soon