<%inherit file="local:templates.master"/>

<%def name="title()">
  Artists Page test
</%def>



<div>
    <h2>Artists DataBase</h2>

    ${c.get_all_form.display(value=artists) | n}
    
</div>
<br/><br/><br/>
