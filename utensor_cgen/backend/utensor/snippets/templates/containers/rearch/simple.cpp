using namespace uTensor;

static localCircularArenaAllocator<{{meta_data_pool_size}}> meta_allocator;
static localCircularArenaAllocator<{{ram_data_pool_size}}> ram_allocator;

{#ex: rom tensors, ops..etc#}
// start rendering global declare snippets
{%for snippet in declare_global_snippets%}
{{snippet.render()}}
{%endfor%}
// end of rendering global declare snippets

void compute_{{model_name}}({%for pl in placeholders%}Tensor& {{pl}}, {%endfor%}{%for out_tensor in out_tensor_var_names%}Tensor& {{out_tensor}}{%if not loop.last%}, {%endif%}{%endfor%}){
    Context::get_default_context()->set_metadata_allocator(&meta_allocator);
    Context::get_default_context()->set_ram_data_allocator(&ram_allocator);
    {#ex: ram tensors#}
    // start rendering local declare snippets
    {%for snippet in declare_local_snippets%}
    {{snippet.render()}}
    {%endfor%}
    // end of rendering local declare snippets
    // start rendering eval snippets
    {%for snippet in eval_snippets%}
    {{snippet.render()}}
    {%if not loop.last%}

    {%endif%}
    {%endfor%}
    // end of rendering eval snippets
}
