<template>
    <div>
        <h1>Book Details</h1>
        <div v-if="book">
            <h2>{{ book.book_name }}</h2>
            <p><strong>Book Name:</strong> {{ book.book_name }}</p>
            <p><strong>Author:</strong> {{ book.author }}</p>
            <!-- Add more details if needed -->
            <button @click="downloadBook" class="action-button pay-button">
                <i class="fas fa-download"></i> Download
            </button>
        </div>
        <div v-else>
            <p>Loading...</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
export default {
    data() {
        return {
            book: null,
            token: null,
        };
    },
    mounted() {
        this.fetchToken();
    },
    methods: {
        async fetchToken() {
            try {
                const token = localStorage.getItem('authToken');
                this.token = token;
                this.fetchBookDetails();
            } catch (error) {
                console.error('Error fetching token:', error);
            }
        },
        async fetchBookDetails() {
            try {
                const bookId = this.$route.params.book_id; // Extract book ID from route params
                const config = {
                    headers: {
                        'Authorization': `Bearer ${this.accesstoken}` // Include the token in the headers
                    }
                };
                const response = await axios.get(`http://127.0.0.1:5000/api/books/${bookId}`, config);
                console.log(response);
                this.book = response.data;
            } catch (error) {
                console.error('Error fetching book details:', error);
            }
        },
        async downloadBook() {
  try {
    if (!this.book) return;

    const bookContent = this.book.path; // Assuming this contains the book content (HTML)
    
    // Create a new jsPDF instance
    const pdf = new jsPDF('p', 'pt', 'a4');

    // Get the HTML element containing the book content
    const bookElement = document.createElement('div');
    bookElement.innerHTML = bookContent;
    console.log(bookElement)

    // Convert the HTML element to a canvas and add it to the PDF
    html2canvas(bookElement, {
      scale: 2,
      useCORS: true,
    }).then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const imgProps = pdf.getImageProperties(imgData);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);

      // Save the PDF file and initiate the download
      pdf.save(`${this.book.book_name}.pdf`);
    });
  } catch (error) {
    console.error('Error downloading book:', error);
  }
},
    }
};

</script>

<style scoped>
/* Button styles */
.pay-button {
    background-color: #28a745;
    color: white;
}
</style>