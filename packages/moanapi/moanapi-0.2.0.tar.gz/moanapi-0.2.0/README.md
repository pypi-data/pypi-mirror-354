# Moan API Python Client (Dynamic Version)

A simple and intuitive Python wrapper for the [Moan API](https://moanapi.ddns.net/).

This package features a dynamic loader for its API modules and an automatic update checker.

## Installation

Install the package directly from PyPI:

    pip install moanapi

## Usage

First, import and initialize the client with your API key. The client will automatically load all available API categories.

    import moanapi

    try:
        client = moanapi.Client(api_key="YOUR_API_KEY")

        # Access dynamically loaded API modules
        quote = client.utility.get_quote(category="anime")
        print(quote['quote'])

        user = client.roblox.get_user_info(user_id=261)
        print(f"Username: {user['data']['username']}")
        
        image_data = client.generative.get_flux_image(prompt="a powerful cat wizard")
        print(f"Image URL: {image_data['image_url']}")

    except moanapi.APIError as e:
        print(f"An API error occurred: {e}")


For a full list of available functions and to check for new updates, use the built-in help function:

    import moanapi

    moanapi.help()


## License
This project is licensed under the MIT License.
