<div class="${w.css_class}">
		<div style="text-align: center; ">${w.text}</div>
        ${w.children[0].display() | n}
		<div style="height: 10px; "></div>
		<div class="rating_bar">
            <div style="width:${w.children[2].value}%" height: 12px;></div>
        </div>
        <br clear="all" />
		${w.children[1].display() | n}
</div>
