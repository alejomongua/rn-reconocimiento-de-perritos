<template>
    <div class="image-upload flex flex-col items-center justify-center p-4">
        <!-- Input oculto para seleccionar archivos -->
        <input type="file" accept="image/*" @change="onFileChange" ref="fileInput" class="hidden" />

        <!-- Botón para abrir el diálogo de selección de archivos -->
        <button @click="triggerFileInput"
            class="btn-upload bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Seleccionar una imagen
        </button>

        <!-- Mostrar la imagen seleccionada -->
        <div v-if="imageUrl" class="mt-4">
            <img :src="imageUrl" alt="Imagen Seleccionada" class="max-w-xs mx-auto" />
            <!-- Muestre el botón solo si no hay classificationResults -->
            <button @click="uploadImage" v-if="!classificationResult"
                class="btn-classify bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-8">
                Encontrar la raza
            </button>
        </div>

        <!-- Mostrar los resultados de clasificación -->
        <div v-if="classificationResult" class="results mt-4">
            <h2 class="text-lg font-bold">Resultados de Clasificación:</h2>
            <ul>
                <li v-for="[breed, probability] in classificationResult" :key="breed">
                    {{ breed }}: {{ probability }}%
                </li>
            </ul>
        </div>
        <div v-if="showModal" class="modal">
            <div class="modal-content">
                Procesando...
            </div>
        </div>

        <!-- Mostrar mensaje de error si existe -->
        <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'ImageUpload',
    setup() {
        const selectedFile = ref<File | null>(null);
        const imageUrl = ref<string | null>(null);
        type ClassificationResult = [string, string][];
        const classificationResult = ref<ClassificationResult | null>(null);
        const showModal = ref(false); // Controla la visibilidad del modal
        const errorMessage = ref<string | null>(null); // Almacena el mensaje de error
        const fileInput = ref<HTMLInputElement | null>(null);

        function triggerFileInput() {
            if (fileInput.value)
                fileInput.value.click();
        }


        function onFileChange(event: Event) {
            const input = event.target as HTMLInputElement;
            if (input.files && input.files[0]) {
                selectedFile.value = input.files[0];

                // Leer el archivo y convertirlo en una URL
                const reader = new FileReader();
                reader.onload = (e) => {
                    if (e.target) {
                        imageUrl.value = e.target.result as string; // Asigna la URL resultante
                    }
                };
                reader.readAsDataURL(selectedFile.value);
                classificationResult.value = null; // Reinicia los resultados de clasificación
            }
        }

        async function uploadImage() {
            if (selectedFile.value) {
                showModal.value = true; // Muestra el modal
                errorMessage.value = null; // Reinicia el mensaje de error
                const formData = new FormData();
                formData.append('file', selectedFile.value);

                try {
                    const response = await fetch('/api/classify', {
                        method: 'POST',
                        body: formData,
                    });

                    // Si el código de error es 413 es porque la imagen tiene muy alta resolución
                    if (response.status === 413) {
                        errorMessage.value = 'La imagen es demasiado grande. Inténtalo de nuevo con una menor resolución.';
                        return;
                    }

                    // Asumiendo que la respuesta es un arreglo de arreglos con [string, number]
                    const data: [string, number][] = await response.json();

                    let totalProbability = 0;
                    const processedData: ClassificationResult = data.map(([breed, probability]) => {
                        const probPercentage = (probability * 100).toFixed(1);
                        totalProbability += probability;
                        return [breed, probPercentage];
                    });

                    if (totalProbability < 0.99) {
                        processedData.push(["Otras razas", ((1 - totalProbability) * 100).toFixed(1)]);
                    }

                    classificationResult.value = processedData;
                } catch (error) {
                    errorMessage.value = 'Error al procesar la imagen. Inténtalo de nuevo.'; // Maneja errores
                    classificationResult.value = null;
                } finally {
                    showModal.value = false;
                }
            }
        }

        return {
            onFileChange,
            uploadImage,
            imageUrl,
            classificationResult,
            showModal,
            errorMessage,
            fileInput,
            triggerFileInput,
        };
    },
});
</script>

<style scoped>
.modal {
    position: fixed;
    /* Fijo en la pantalla */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    /* Centrado horizontal */
    align-items: center;
    /* Centrado vertical */
    background-color: rgba(0, 0, 0, 0.5);
    /* Fondo semitransparente */
    z-index: 1000;
    /* Asegúrate de que esté sobre otros elementos */
}

.modal-content {
    padding: 20px;
    background-color: white;
    border-radius: 10px;
    /* Bordes redondeados */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    /* Sombra sutil */
}

.error-message {
    padding: 10px;
    margin-top: 10px;
    background-color: #ffdddd;
    /* Fondo rojo claro */
    border: 1px solid #ff0000;
    /* Borde rojo */
    border-radius: 5px;
    /* Bordes redondeados */
    color: #ff0000;
    /* Texto rojo */
    text-align: center;
}
</style>
