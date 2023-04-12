# How to run
## Step 1. Creating a Spotify Account
Spotipy relies on the Spotify API. In order to use the Spotify API, you'll need to create a Spotify developer account.

1. Head over to the Spotify developer portal at https://developer.spotify.com/dashboard/. If you're new to Spotify, create an account by clicking the "Sign up" button and following the instructions. If you already have a Spotify account, simply log in with your credentials to access your developer dashboard.

2. Once you're logged in, click the "Create an App" button and provide a name and description for your app. You'll also need to agree to the terms of service before you can proceed. Once you're done, click "Create" to proceed.

3. On the Overview screen of your new app, click the "Edit Settings" button and scroll down until you see the "Redirect URIs" section. Here, you'll need to add "http://localhost:1234" (or any other port number you prefer). Once you've added the URI, click "Save" to return to the Overview screen.

4. To access your Client ID and Client Secret, navigate to the left-hand side of the Overview screen where you'll see your app name and description. Click the "Show Client Secret" link, and both your Client ID and Client Secret will be revealed. Make sure to copy them down somewhere safe as you'll need them later on.


## Step 2. Installation and Setup

1. export environment variables 
The values for these variables are the ones you created for you App in Step 1
```
Linux or Mac
export SPOTIPY_CLIENT_ID=client_id_here
export SPOTIPY_CLIENT_SECRET=client_secret_here
export SPOTIPY_REDIRECT_URI="eredirect_uri_here"

# Windows
$env:SPOTIPY_CLIENT_ID="client_id_here"
$env:SPOTIPY_CLIENT_SECRET="client_secret_here"
$env:SPOTIPY_REDIRECT_URI="redirect_uri_here"
```


2. Install requirements with `pip install -r requirements.txt`


## Step 3. Run the script
Now you should be able to run 
```
python save_discover_weekly.py
```
You may be prompted to login to Spotify's OAuth or if you are already logged into Spotify in your browser it may use the exising session.

A playlist called `<Monday of this week> discover weekly (ReDiscover Weekly)` should have been created with the songs of your current discover weekly.

NOTE: By default Spotipy will create a `.cache` file to cache your access tokens.
