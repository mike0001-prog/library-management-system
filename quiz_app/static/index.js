// function Quiz(question,option_one,option_two,option_three,answer) {
//     this.question = question
//     this.option_one = option_one
//     this.option_two = option_two
//     this.option_three = option_three
//     this.answer = answer
// }
// const  quiz_one = new Quiz("how many days are in a year","365","365.5","364","365")
// const  quiz_two = new Quiz("how many weeks are in a year","52","51","53","52")
// const container = document.querySelector(".question-wrapper")
// const arr = [quiz_one,quiz_two]
// const Mount = (question)=>{
// return ( `  <div class="question">
//                 ${question.question}
//             </div>
//             <form action="http://127.0.0.1:8000/test/" method=post>
//             <ul>
//                 <li style="list-style: none;">A
//                 <input id="option_one" type="radio" name=.addEventListener("click",function () {
//     console.log("test")
// }) value=${question.option_one}>
//                 <label for="option_one">${question.option_one}</label>
//                 </li>
//                 <li style="list-style:none;">B
//                 <input id="option_two" type="radio" name="option_two" value=${question.option_two}>
//                 <label for="option_two">${question.option_two}</label>
//                 </li>
//                 <li style="list-style:none;">C
//                 <input id="option_three" type="radio" name="option_three" value=${question.option_three}>
//                 <label for="option_three">${question.option_three}</label>
//                 </li>
//             </ul>
//             <button> submit</button>
//             </form>
//             `)
// }
// const store =  sessionStorage
// const store__arr = {1:"bad"}

// store.setItem("key",JSON.stringify(store__arr))
// container.innerHTML = Mount(arr[0])
// const btns = document.querySelectorAll("input")
// const option_one = document.querySelector("#option_one")
// const option_two = document.querySelector("#option_two")
// const option_three = document.querySelector("#option_three")
// btns.forEach((btn)=>{
//     btn.addEventListener("click",function () {
//     if ((btn.id == "option_one")  ){
//         console.log("option_one")
//         option_two.checked = false
//         option_three.checked = false
//     }else if((btn.id == "option_two")){
//         option_one.checked = false
//         option_three.checked = false
//     }else if((btn.id == "option_three")){
//         option_one.checked = false
//         option_two.checked = false
//     }
// })
// })   dfcj


        // document.addEventListener('DOMContentLoaded', function() {

            
        //     // Hide modal when clicking outside the alert box
        //     modalOverlay.addEventListener('click', function(e) {
        //         if (e.target === modalOverlay) {
        //             hideModal();
        //         }
        //     });
            
        //     // Hide modal when pressing Escape key
        //     document.addEventListener('keydown', function(e) {
        //         if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
        //             hideModal();
        //         }
        //     });
        // });




        
const sessionstorage = sessionStorage
const condition = sessionstorage.getItem("condition")
const modalOverlay = document.getElementById('modalOverlay');
const closeModal = document.getElementById('closeModal');
function showModal() {
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}
if(condition === "no"){
    hideModal()
}else{
    showModal()
}
function hideModal() {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = ''; // Re-enable scrolling
    sessionstorage.setItem("condition","no")
}
closeModal.addEventListener('click', hideModal);
if(sessionstorage.getItem("condition") === "no"){
sessionstorage.getItem("answered_question")
}else{
    sessionstorage.setItem("answered_question",JSON.stringify({}))
}



function ChangeSelectbtnState(){
    const answered_question = JSON.parse(store.getItem("answered_question"))
    const keys = Object.keys(answered_question)
    console.log(keys)
    const btns = document.querySelectorAll(".sub-layout button")
    // const index = sessionstorage.getItem("current")
    // const el = document.getElementById(`${index}`)
    // el.classList.remove("btn-danger")
    // el.classList.add("btn-success")
    keys.forEach((key)=>{
    const el = document.getElementById(`${key}`)
    el.classList.remove("btn-danger")
    el.classList.add("btn-success")
    })
    // for(let i=0;i<=btns.length;i++){
    //     let val = parseInt(btns[i].innerHTML)-1
    //      if(val in keys){
    //         // btns[i].classList.remove("btn-danger")
    //         // btns[i].classList.add("btn-success")
    //         const el = document.querySelector(`#${i}`)
    //         console.log("pass")
    //     }else{
    //         console.log("fail")
    //     }
    }
   


$(function () {
    $('.question-wrapper').on('change', 'form', function(e) {
    const $option = $(this); 
    const c = parseInt(sessionstorage.getItem("current"))
    console.log(typeof c)
    // const question_index = $option.attr("data-index")
    const answer = e.target.value
    console.log(answer)
    const storeAnswer = JSON.parse(sessionstorage.getItem("answered_question"))
    console.log(typeof storeAnswer)
    storeAnswer[c]= answer
    console.log(storeAnswer)
    sessionstorage.setItem("answered_question",JSON.stringify(storeAnswer))
    ChangeSelectbtnState()
    console.log(typeof sessionstorage.getItem("answered_question"))
    // const stringifyAnswer = JSON.stringify(storeAnswer)
    // const sessionstorage = sessionStorage
    // sessionstorage.setItem("answered_question",stringifyAnswer)
    // console.log(sessionstorage.getItem("answered_question"))
// console.log($option.serialize())
    $.ajax({
        
    url:$option.attr("action"),
    data:$option.serialize(),
    type:$option.attr("method"),
    success:function(response){
        if(response){
            console.log(response)
        }
    }
})
})
// clear storage
$('#modalOverlay').on('submit', 'form', function() {
    sessionstorage.clear()
})
})




// $(document).ready(function() {
//     const quizData = [/* your questions */];
//     let currentQuestionIndex = 0;
    
//     // Initialize with event delegation
//     $('#options-container').on('click', '.option', function() {
//         const $option = $(this);
        
//         // Clear previous selections
//         $('.option').removeClass('selected');
        
//         // Mark current selection
//         $option.addClass('selected');
        
//         // Enable next button
//         $('#next-btn').prop('disabled', false);
//     });
    
//     function loadQuestion() {
//         const question = quizData[currentQuestionIndex];
        
//         // Update question text
//         $('#question').text(question.text);
        
//         // Clear and rebuild options
//         $('#options-container').empty();
//         question.options.forEach((opt, idx) => {
//             $('<div>')
//                 .addClass('option')
//                 .data('index', idx)
//                 .text(opt)
//                 .appendTo('#options-container');
//         });
        
//         // Reset UI state
//         $('#next-btn').prop('disabled', true);
//     }
    
//     $('#next-btn').click(function() {
//         currentQuestionIndex++;
//         if (currentQuestionIndex < quizData.length) {
//             loadQuestion();
//         } else {
//             // Quiz complete
//         }
//     });
    
//     // Start quiz
//     loadQuestion();
// });



 