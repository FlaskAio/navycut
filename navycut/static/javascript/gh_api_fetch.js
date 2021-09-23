fetch("https://api.github.com/repos/flaskAio/navycut").then(res=>res.json()).then(repo=>{
    document.getElementById("intro__desc").innerHTML = repo.description;
    document.getElementById("github__star").innerHTML = repo.stargazers_count;
    document.getElementById("github__watch").innerHTML = repo.watchers;
    document.getElementById("github__forks").innerHTML = repo.forks_count;
})

fetch("https://api.github.com/repos/flaskAio/navycut/contributors?per_page=1&anon=true")
    .then(res => res.headers).then(headers => {
        headers.forEach((value, key) => {
            if (key === 'link') {
                const contributors = value.split(",")[1].split(";")[0].split("&").slice(-1)[0].slice(5, -1);
                document.getElementById("github__contributors").innerHTML = contributors;
            }
        })
    })