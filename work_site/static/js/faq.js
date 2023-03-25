        const faqs = document.querySelectorAll(".faq");
        for (const item of faqs) {
            const curr_faq = item.childNodes;
            console.log(curr_faq);
            const question = curr_faq[1];
            const answer = curr_faq[3];
            const icon = question.querySelector(".icon-main");
            icon.addEventListener("click", function () {
                answer.classList.toggle("non-active");
                const i = icon.querySelector("i");
                i.classList.toggle("fa-xmark");
                i.classList.toggle("fa-plus");
            });
        }