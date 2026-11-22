/*
  The Unassuming Tavern: where the three doors lead.
  This is the only file you edit to wire up your domain. Leave a value '' to keep that door locked
  (the button still shows; pressing it just says the door is barred).

  How the link for each door is chosen:
    1. domain + subdomain both set  ->  https://<subdomain>.<domain>/
    2. otherwise, githubPage set    ->  that address (use it until the custom subdomain works)
    3. otherwise                    ->  locked

  Also set the same domain in a file named CNAME at the repo root (just the domain, one line)
  and in Settings > Pages of this repo. See README.md, "Domain setup".
*/
window.TAVERN_CONFIG = {
  // Your custom domain, no https:// and no trailing slash. Example: 'example.com'
  domain: '',

  sites: [
    {
      id: 'poly-runner',
      label: 'Poly Runner',
      subdomain: '',   // the part before the domain. Example: 'run'  ->  https://run.example.com/
      githubPage: '',  // Example: 'https://<your-github-name>.github.io/<repo-name>/'
    },
    {
      id: 'bloodsoup-hell',
      label: 'Bloodsoup Hell',
      subdomain: '',
      githubPage: '',
    },
    {
      id: 'lifebrained',
      label: 'Lifebrained',
      subdomain: '',
      githubPage: '',
    },
  ],
};
