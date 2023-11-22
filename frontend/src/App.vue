<template>
  <div class="dark:bg-gray-800 dark:text-white"> <!-- Fondo oscuro y texto claro -->
    <div class="container mx-auto p-4">
      <div class="text-center">
        <img src="@/assets/logo.png" alt="Logo" class="mx-auto" />
        <!-- Asegúrate de reemplazar con la ruta correcta a tu logo -->
        <h1 class="text-2xl font-bold my-4">Identifica la raza de tu mejor amigo</h1>
        <p class="mb-4">Sube una foto de tu perro y descubre su raza.</p>
        <ImageUpload />
        <div v-if="image" class="my-4">
          <img :src="image" alt="Imagen del Perro" class="mx-auto" />
        </div>
        <div v-if="classificationResult" class="my-4">
          <h2 class="text-xl font-semibold">Resultado de la Clasificación:</h2>
          <p>{{ classificationResult }}</p>
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
