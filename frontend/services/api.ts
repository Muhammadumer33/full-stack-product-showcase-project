import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface Product {
    id?: number;
    name: string;
    description: string;
    price: number;
    category: string;
    brand: string;
    stock: number;
    rating?: number;
    image_path?: string;
    created_at?: string;
}

// Get all products
export const getProducts = async (category?: string, search?: string) => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);

    const response = await axios.get(`${API_URL}/products?${params.toString()}`);
    return response.data;
};

// Get single product
export const getProduct = async (id: number) => {
    const response = await axios.get(`${API_URL}/products/${id}`);
    return response.data;
};

// Create product with image
export const createProduct = async (productData: Product, imageFile?: File) => {
    const formData = new FormData();
    formData.append('name', productData.name);
    formData.append('description', productData.description);
    formData.append('price', productData.price.toString());
    formData.append('category', productData.category);
    formData.append('brand', productData.brand);
    formData.append('stock', productData.stock.toString());
    formData.append('rating', (productData.rating || 0).toString());

    if (imageFile) {
        formData.append('image', imageFile);
    }

    const response = await axios.post(`${API_URL}/products`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// Update product
export const updateProduct = async (id: number, productData: Partial<Product>, imageFile?: File) => {
    const formData = new FormData();

    if (productData.name) formData.append('name', productData.name);
    if (productData.description) formData.append('description', productData.description);
    if (productData.price) formData.append('price', productData.price.toString());
    if (productData.category) formData.append('category', productData.category);
    if (productData.brand) formData.append('brand', productData.brand);
    if (productData.stock !== undefined) formData.append('stock', productData.stock.toString());
    if (productData.rating !== undefined) formData.append('rating', productData.rating.toString());

    if (imageFile) {
        formData.append('image', imageFile);
    }

    const response = await axios.put(`${API_URL}/products/${id}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// Delete product
export const deleteProduct = async (id: number) => {
    const response = await axios.delete(`${API_URL}/products/${id}`);
    return response.data;
};

// Get categories
export const getCategories = async () => {
    const response = await axios.get(`${API_URL}/categories`);
    return response.data;
};

// Change password
export const changePassword = async (currentPassword: string, newPassword: string) => {
    const response = await axios.post(`${API_URL}/change-password`, {
        current_password: currentPassword,
        new_password: newPassword
    });
    return response.data;
};

// ===== USER MANAGEMENT =====

export interface User {
    id: number;
    email: string;
    name?: string;
}

// Get all users
export const getUsers = async () => {
    const response = await axios.get(`${API_URL}/users`);
    return response.data;
};

// Create user
export const createUser = async (email: string, name: string, password: string) => {
    const response = await axios.post(`${API_URL}/users`, {
        email,
        name,
        password
    });
    return response.data;
};

// Update user
export const updateUser = async (userId: number, email?: string, name?: string, password?: string) => {
    const response = await axios.put(`${API_URL}/users/${userId}`, {
        email,
        name,
        password
    });
    return response.data;
};

// Delete user
export const deleteUser = async (userId: number) => {
    const response = await axios.delete(`${API_URL}/users/${userId}`);
    return response.data;
};

// Update own profile
export const updateProfile = async (email?: string, name?: string) => {
    const response = await axios.put(`${API_URL}/profile`, {
        email,
        name
    });
    return response.data;
};