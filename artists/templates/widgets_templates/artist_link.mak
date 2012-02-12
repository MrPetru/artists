<div class="${w.css_class}">
    % if (w.value != None):
        <a href="${w.value or ''}" target="_blank">${w.text}</a>
    % else:
        ${w.text}
    % endif
</div>
