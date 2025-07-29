import{j as r}from"./index-DtxP6EWh.js";import"./index-D4AkeOnM.js";import"./svelte/svelte.js";const e="passPixelShader",a=`varying vec2 vUV;uniform sampler2D textureSampler;
#define CUSTOM_FRAGMENT_DEFINITIONS
void main(void) 
{gl_FragColor=texture2D(textureSampler,vUV);}`;r.ShadersStore[e]||(r.ShadersStore[e]=a);const s={name:e,shader:a};export{s as passPixelShader};
//# sourceMappingURL=pass.fragment-Dly2nFsW.js.map
