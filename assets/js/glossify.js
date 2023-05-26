fetch('/library//assets/glossary.json')
.then((response) => response.json())
.then((glossary) => {
        glossary = glossary 

        var glossary_items = document.getElementsByClassName("glosstag");
        for (var i = 0; i < glossary_items.length; i++) {

            glossary_items.item(i).onmouseover = function () {
                var defbox = document.getElementById('defbox')
                defbox.style.display = 'block'

                defbox.style.width = (this.offsetWidth + 40) + 'px'
                defbox.style.top = (this.offsetTop - 220) + 'px'
                defbox.style.left = (this.offsetLeft - 20) + 'px'
                
                document.getElementById('defbox-text').innerHTML = '<p><u><b>' + this.dataset.key + '</u></b></p>' + glossary[this.dataset.key].definition
                console.log(this.dataset.key)
                console.log(glossary[this.dataset.key])
            }
        }
    }
)