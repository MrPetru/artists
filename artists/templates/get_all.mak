<%inherit file="local:templates.master"/>

<%def name="title()">
  Artists Page test
</%def>



<div>
    <h2>Artists DataBase</h2>
    <table class="artist-list">
        <thead>
            <tr>
            <th width=100px>Nome</th><th width=100px>Cognome</th>
            <th width=100px>Ruolo</th><th width=100px>Software</th>
            <th width=100px>SITE-Link</th><th width=100px>REEL-Link</th>
            <th width=100px>Phone</th><th width=100px>E-mail</th>
            <th width=100px>Skype</th><th width=100px>CV</th>
            <th width=100px>Note</th><th width=100px>Tags</th>
            </tr>
        </thead>
        <tbody>
            % for art in artists:
            <tr>
                <td >${art.firstname}</td>
                <td >${art.lastname}</td>
                <td >
                    %for r in art.role:
                        ${r.name};
                    %endfor
                </td>
                <td >
                    % for s in art.software:
                        ${s.name}
                    %endfor
                </td>
                <td >${art.sitelink}</td>
                <td >${art.reellink}</td>
                <td >
                    %for p in art.phone:
                        ${p.phone};
                    %endfor
                </td>
                <td >
                    %for e in art.email:
                        ${e.email};
                    %endfor
                </td>
                <td >
                    %for s in art.skype:
                        ${s.skype};
                    %endfor
                </td>
                <td >
                    ${art.cvlocal}
                </td>
                <td >
                    ${art.note}
                </td>
                <td >
                    %for t in art.tags:
                        ${t.name};
                    %endfor
                </td>
            </tr>
            <tr>
            </tr>
            % endfor
        </tbody>
    </table>
</div>
<br/><br/><br/>
