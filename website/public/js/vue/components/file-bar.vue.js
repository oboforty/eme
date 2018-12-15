export const template = `
  
  <div>
    
    <span v-for="part in path_parts">

      <button class="btn btn-sm btn-link" v-on:click="onClicked(part.path)">
        {{ part.folder }}
      </button>

      /
    </span>
    <!--
    

list of <a> 1 per slash :: button: megnyit mappa
feher area click: hides
and show input with vpath


    -->
  </div>
`;