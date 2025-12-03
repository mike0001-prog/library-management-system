// let links = document.querySelectorAll(".contact_link")
// console.log(links);


// for(i = 0; i <= links.length - 1; i++){
//     let each_href = links[i]
//     console.log(each_href);
//     each_href.addEventListener("click", e =>{     
//         e.preventDefault()
//         let xhr = new XMLHttpRequest()
//         let url = each_href.href

//         xhr.open("GET", url, true)

//         xhr.onreadystatechange = ()=>{
//             let parent = document.querySelector(".chat_right_right")
//             console.log(parent);
            
//             if(xhr.readyState == 4 || xhr.status == 200){
//                 parent.innerHTML = xhr.responseText
//             }
//         }
//         xhr.send()  
//     })
// }


// let viewoption = document.getElementById("view_option")
let viewoption = document.querySelectorAll(".vopt")
let more_option = document.querySelectorAll(".more_option")
let title = document.querySelectorAll(".fw-bolder")


for (let index = 0; index <= viewoption.length - 1; index++) {
    const element = viewoption[index];
    let arr = [viewoption[index]]   
    for( i = 0; i <= more_option.length - 1; i++){
        const ele = more_option[i]
    }
}

// for (let i, j, k = 0; i <= viewoption.length - 1, j <= more_option.length - 1, k <= title.length - 1; i, j, k ++) {
//     console.log(i,j,k);
    
// }
