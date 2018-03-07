<%text><%inherit file="/T/search_base.html"/>
<%block name="search_body">
</%text>
<div class="form-group">
    %for rec in recs:
    <label class="col-sm-2 control-label">${rec.colcomment}</label>
    <div class="col-sm-4">
        <input type="text" v-model="row.${rec.colname}" name="${rec.colname}" class="form-control">
    </div>
    %endfor
</div>
<%text>
</%block>
</%text>