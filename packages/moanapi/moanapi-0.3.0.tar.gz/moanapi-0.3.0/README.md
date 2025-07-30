# Moan API Python Client (Dynamic Version)

A simple and intuitive Python wrapper for the [Moan API](https://moanapi.ddns.net/).

This package features a dynamic loader for its API modules and an automatic update checker.

## Installation

Install the package directly from PyPI:

    pip install moanapi

## Usage

First, import and initialize the client with your API key. It's conventional to name the client instance `moan`.

    import moanapi

    try:
        moan = moanapi.Client(api_key="YOUR_API_KEY")

        # Get an anime quote
        quote = moan.utility.get_quote(category="anime")
        print(quote['quote'])

        # Get Roblox user info
        user = moan.roblox.get_user_info(user_id=261)
        print(f"Username: {user['data']['username']}")
        
        # Generate an image with AI
        image_data = moan.generative.get_flux_image(prompt="a powerful cat wizard")
        print(f"Image URL: {image_data['image_url']}")

        # Generate a rankcard (returns raw image bytes)
        image_bytes = moan.generative.generate_rankcard(
            username="Zlan", avatar="AVATAR_URL", current_xp=900, 
            next_level_xp=1000, level=24, rank=1
        )
        with open("rankcard.png", "wb") as f:
            f.write(image_bytes)

    except moanapi.APIError as e:
        print(f"An API error occurred: {e}")


For a full list of available functions and to check for new updates, use the built-in help function:

    import moanapi

    moanapi.help()


## License
This project is licensed under the MIT License.
