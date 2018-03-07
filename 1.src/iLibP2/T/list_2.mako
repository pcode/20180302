<%text><%inherit file="/T/rowedit_base.html"/>
<%block name="data_body">
</%text>
<div class="form-group">
    %for rec in recs:
    <label class="col-sm-2 control-label">${rec.colcomment}</label>
    <div class="col-sm-4">
        <input type="text" v-model="row.${rec.colname}" id="${rec.colname}" name="${rec.colname}" class="form-control">
    </div>
    %endfor
</div>
<div class="hr-line-dashed"></div>
<%text></%block></%text>
