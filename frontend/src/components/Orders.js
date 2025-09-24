import {Wrapper} from "./Wrapper";
import {useEffect, useState} from "react";

export const Orders = () => {
    const [selectedProductId, setSelectedProductId] = useState('');
    const [quantity, setQuantity] = useState('');
    const [message, setMessage] = useState('Select a product to see pricing');
    const [products, setProducts] = useState([]);

    // Load products on component mount
    useEffect(() => {
        (async () => {
            try {
                const response = await fetch('${INVENTORY_SERVICE_URL}/products');
                const content = await response.json();
                setProducts(content);
            } catch (e) {
                console.error('Failed to load products:', e);
            }
        })();
    }, []);

    // Update message when product is selected
    useEffect(() => {
        (async () => {
            try {
                if (selectedProductId) {
                    const response = await fetch(`${INVENTORY_SERVICE_URL}/products/${selectedProductId}`);
                    const content = await response.json();
                    const price = parseFloat(content.price) * 1.2;
                    setMessage(`Your product price is $${price.toFixed(2)}`);
                } else {
                    setMessage('Select a product to see pricing');
                }
            } catch (e) {
                setMessage('Error loading product details');
            }
        })();
    }, [selectedProductId]);

    const submit = async e => {
        e.preventDefault();

        if (!selectedProductId || !quantity) {
            setMessage('Please select a product and enter quantity');
            return;
        }

        try {
            const response = await fetch('${PAYMENT_SERVICE_URL}/orders', {
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify({
                    id: selectedProductId, 
                    quantity: parseInt(quantity)
                })
            });

            if (response.ok) {
                setMessage('Thank you for your order!');
                setSelectedProductId('');
                setQuantity('');
            } else {
                const error = await response.json();
                setMessage(`Error: ${error.detail || 'Order failed'}`);
            }
        } catch (e) {
            setMessage('Error placing order. Please try again.');
        }
    }

    return <Wrapper>
        <main>
            <div className="py-5 text-center">
                <h2>Checkout form</h2>
                <p className="lead">{message}</p>
            </div>

            <form onSubmit={submit}>
                <div className="row g-3">
                    <div className="col-sm-6">
                        <label className="form-label">Product</label>
                        <select className="form-select" 
                                value={selectedProductId}
                                onChange={e => setSelectedProductId(e.target.value)}>
                            <option value="">Select a product...</option>
                            {products.map(product => (
                                <option key={product.id} value={product.id}>
                                    {product.name} - ${product.price} (Qty: {product.quantity})
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="col-sm-6">
                        <label className="form-label">Quantity</label>
                        <input type="number" 
                               className="form-control"
                               value={quantity}
                               onChange={e => setQuantity(e.target.value)}
                               min="1"
                               required />
                    </div>
                </div>
                <hr className="my-4"/>
                <button className="w-100 btn btn-primary btn-lg" type="submit">Buy</button>
            </form>
        </main>
    </Wrapper>
}