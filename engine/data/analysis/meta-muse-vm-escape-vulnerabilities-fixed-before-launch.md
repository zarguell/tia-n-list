In the weeks immediately before launch, Meta engineers found several security vulnerabilities in Muse, the company's AI agent product, including VM escape flaws that could have let users break out of the product's sandbox into Meta's internal systems. According to 404 Media's reporting, the flaws were rushed to fix ahead of release rather than delaying the launch.

The reason this deserves attention is the threat model it reveals. Muse is a consumer-facing agent that executes code on Meta's infrastructure, which makes the boundary between user workload and corporate network the single most consequential control in the product. VM escape findings so close to launch suggest that boundary was under real pressure, and that launch timing won out over a full hardening cycle.

Most AI agent products today are in the same position: sandboxes borrowed from earlier eras of multi-tenancy, pointed at hostile users who have economic motivation to escape. Meta moving fast and fixing in place is a reasonable response, but it converts early customers into an unwitting test population.

Watch for post-launch escape research against Muse, any Meta disclosure of additional flaws found after release, and whether the company isolates the product away from internal systems. Similar scrutiny will land on every agent platform that blends user-supplied code with corporate adjacency.
