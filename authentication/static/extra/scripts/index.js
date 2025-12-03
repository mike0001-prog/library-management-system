const id_avatar = document.getElementById("id_avatar")
const update_img = document.getElementById("update_img")
const user_img = document.getElementById("user_img")

// user_img.addEventListener("click", ()=>{
//     user_img.src = id_avatar.value
// })

const links = document.getElementsByName("links")
for(i = 0; i <= links.length - 1; i++){
    const link = links[i]
    link.addEventListener("click", e =>{
        e.preventDefault()

        const xhr = new XMLHttpRequest()
        const url = link.href
        xhr.open("GET", url, true)

        xhr.onload = ()=>{
            if(xhr.readyState == 4 || xhr.status == 200){
                let side_right = document.querySelector(".side_right")
                side_right.style.width ="40%"
                side_right.style.height ="83.7vh"
                side_right.style.background ="#88888885"
                side_right.style.transition ="all .4s ease-in"
                side_right.innerHTML = xhr.responseText
            }
        }

        xhr.send()

    })
}