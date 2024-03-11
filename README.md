# Sort your Spotify playlist's songs with **SpotifyBMMsorter*

### DETAILED INSTRUCTIONS 

### Step 1: Register on Spotify Developer Dashboard

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. If you're not already logged in, log in with your Spotify account. If you don't have an account, you'll need to sign up for one.
3. Once logged in, you'll be on the Dashboard. Click on **CREATE AN APP**.
4. Fill in the **App Name** and **App Description**. Agree to the terms and conditions, and then click **CREATE**.

### Step 2: Get Your API Keys

After creating your app, you'll be directed to your app's dashboard:

1. Here, you'll find your **Client ID**. Keep this ID; you'll need it to authenticate your application with the Spotify API.
2. To get your **Client Secret**, click on **SHOW CLIENT SECRET**. Treat your Client Secret like a password—do not share it publicly.

### Step 3: Set Up a Redirect URI

A Redirect URI is a URL to which Spotify will redirect the user after they authorize (or deny) access to your application. This is crucial for the OAuth authentication flow.

1. On your application's dashboard, click **EDIT SETTINGS**.
2. In the **Redirect URIs** section, you'll add a URI where Spotify will send the user after authorization. For local development, you can use something like `http://localhost:8888/callback`. This URI doesn't need to host an actual web service; it's just used as a callback URL for Spotify's OAuth flow.
3. After adding the URI, click **ADD**, then **SAVE** at the bottom.

### Using the Credentials and Redirect URI in Your Application

With your **Client ID**, **Client Secret**, and **Redirect URI**, you're ready to authenticate your application with Spotify:

- Store these values securely.
- Use the **Client ID** and **Client Secret** in your application to authenticate with the Spotify API.
- The **Redirect URI** will be used in the OAuth flow; ensure it matches exactly what you set in the Spotify app settings, including the port number if specified.

For detailed documentation on Spotify's authorization process and how to use these keys, refer to the [Spotify Web API Authorization Guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/).

### Important Tips:

- **Security**: Keep your Client Secret confidential. If it's exposed, regenerate it immediately from the Spotify Developer Dashboard.
- **Redirect URIs**: If you're developing locally, `http://localhost:port/callback` is typical, but ensure the port matches in your application and Spotify app settings.
- **Scope**: When using Spotipy or other libraries to authenticate, you'll need to specify the right [scopes](https://developer.spotify.com/documentation/general/guides/scopes/) to access certain API features, like modifying playlists.

By following these steps, you'll be able to authenticate your application with Spotify, allowing it to interact with the Spotify API, including fetching and modifying playlists.

### The application saves your API keys, be aware of that! 
