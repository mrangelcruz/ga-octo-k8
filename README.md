This app will have its background color changed via index.html: <br>

        background-color: {{ bg_color }};


This will depend on the environment it is deployed to, the environment variable BG_COLOR will be set to the environment variable:

        bg_color = os.getenv("BG_COLOR", "#ffffff")  # default to white if not set


That environment variable, BG_COLOR, is set in Octopus Deploy for each environment (Development, Staging, and Production).

The port is also environment specific (8080,8081,8082), from the Docker run of this app:


        docker run -d --name flask-app -p #{PORT}:5000 -e BG_COLOR=#{BG_COLOR} mrangelcruz1960/flask-app:#{Octopus.Release.Number}

