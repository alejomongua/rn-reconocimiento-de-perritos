<template>
  <div>
    <div class="container mx-auto p-4 text-center">
      <div>
        <img src="@/assets/logo.png" alt="Logo" class="mx-auto" />
        <!-- Asegúrate de reemplazar con la ruta correcta a tu logo -->
        <h1 class="text-2xl font-bold my-4">Identifica la raza de mascota.</h1>
        <p class="mb-4">
          Sube una foto de tu perro y descubre su raza.
          Las imágenes subidas no serán almacenadas en el servidor, solo se procesarán y se eliminarán.
        </p>
        <ImageUpload />
        <div v-if="image" class="my-4">
          <img :src="image" alt="Imagen del Perro" class="mx-auto" />
        </div>
        <div v-if="classificationResult" class="my-4">
          <h2 class="text-xl font-semibold">Resultado de la Clasificación:</h2>
          <p>{{ classificationResult }}</p>
        </div>
      </div>
      <div class="footer">
        <div class="footer-content">
          <div class="footer-section about">
            Identificando a Firulais
            es un proyecto para la clase de Redes neuronales de 2023-2 de la Universidad Nacional de Colombia
            <div class="contact">
              <div>Autores: lamongual - adariasz - dcocoma</div>
            </div>

            <div class="text-blue-500">
              <a href="https://github.com/alejomongua/rn-reconocimiento-de-perritos" target="_blank">
                <i class="fab fa-github">Código fuente</i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import ImageUpload from './components/ImageUpload.vue';

export default defineComponent({
  name: 'App',
  components: {
    ImageUpload
  },
  setup() {
    const image = ref(null); // URL de la imagen subida
    const classificationResult = ref(null); // Resultado de la clasificación

    // Aquí puedes agregar métodos para manejar la carga de imágenes y la clasificación

    return { image, classificationResult };
  }
});
</script>

<style>
/* Aquí puedes agregar estilos globales con Tailwind */
</style>
