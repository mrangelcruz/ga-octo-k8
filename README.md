This app will have its background color changed via index.html: <br>

        background-color: {{ bg_color }};


This will depend on the environment it is deployed to, the environment variable BG_COLOR will be set to the environment variable:

        bg_color = os.getenv("BG_COLOR", "#ffffff")  # default to white if not set


That environment variable, BG_COLOR, is set in Octopus Deploy for each environment (Development, Staging, and Production).

The port is also environment specific (8080,8081,8082), from the Docker run of this app:


        docker run -d --name flask-app -p #{PORT}:5000 -e BG_COLOR=#{BG_COLOR} mrangelcruz1960/flask-app:#{Octopus.Release.Number}

---

## Gemini Code Assist History

### How to dynamically create SNS topics in Terraform from a config file?

**Question:**

> in my sns/main.tf file, note that I am hardcoding topics when I need to create them.
> Can we refactor this such that when I do a terraform apply, it will open a config file and do actions based on the config file?
>
> For example, I have this config.yml file I use in Pulumi:
> ```yaml
> # config.yml
>
> module:
>  sns:
>    mode: create
>    deploy: true
>    topics:
>      - name: github-actions
>        region:
>          - us-west-2
>        email_subscribers:
>          - mrangelcruz@gmail.com
>          - anghotpekpek@gmail.com
> ```
> Based on this config.yml file, I control what to create and what to set for email subscribers.
> Can I do something like this in terraform instead of hard-coding main.tf?

**Answer:**

Yes, this is a great pattern in Terraform. Instead of hardcoding resources, you can use a configuration file and Terraform's `for_each` meta-argument to create resources dynamically.

The file `/home/angelcruz/repos/ga-octo-k8/terraform/sns/main.tf` was updated to read the topics from `/home/angelcruz/repos/ga-octo-k8/config.yaml`.

The `locals` block in `main.tf` was changed to use `path.root` to reference the project's root directory and load `config.yaml`. The `yamldecode` function parses the YAML file, and we access the `topics` map from it.

The `module "sns_topics"` block then uses `for_each` to iterate over each key-value pair in the `local.topics` map. For each topic in the map, it creates an instance of the `../modules/sns-topic` module, passing the topic name (`each.key`) and its subscribers (`each.value.email_subscribers`) as variables. This makes your SNS topic management declarative and scalable.
