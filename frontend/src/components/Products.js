import { Wrapper } from "./Wrapper";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../assets/styles/Shimmer.css";

export const Products = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true); // Add loading state

    useEffect(() => {
        (async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_INVENTORY_SERVICE_URL}/products`);

                if (!response.ok) {
                    console.error('Failed to fetch products:', response.status);
                    setProducts([]);
                    setLoading(false); // Stop loading on error
                    return;
                }

                const content = await response.json();

                if (Array.isArray(content)) {
                    setProducts(content);
                } else {
                    console.error('Fetched content is not an array:', content);
                    setProducts([]);
                }
            } catch (e) {
                console.error('Error fetching products:', e);
                setProducts([]);
            } finally {
                setLoading(false); // Stop loading after fetch
            }
        })();
    }, []);

    const del = async id => {
        if (window.confirm('Are you sure to delete this record?')) {
            await fetch(`${process.env.REACT_APP_INVENTORY_SERVICE_URL}/products/${id}`, {
                method: 'DELETE'
            });

            setProducts(products.filter(p => p.id !== id));
        }
    }

    const Shimmer = () => (
        <div className="shimmer-wrapper">
            <div className="shimmer"></div>
        </div>
    );

    return (
        <Wrapper>
            <div className="pt-3 pb-2 mb-3 border-bottom">
                <Link to={`/create`} className="btn btn-sm btn-outline-secondary">Add</Link>
            </div>

            <div className="table-responsive">
                <table className="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Price</th>
                            <th scope="col">Quantity</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            Array.from({ length: 5 }).map((_, index) => (
                                <tr key={index}>
                                    <td><Shimmer /></td>
                                    <td><Shimmer /></td>
                                    <td><Shimmer /></td>
                                    <td><Shimmer /></td>
                                    <td><Shimmer /></td>
                                </tr>
                            ))
                        ) : (
                            products.map(product => {
                                return <tr key={product.id}>
                                    <td>{product.id}</td>
                                    <td>{product.name}</td>
                                    <td>{product.price}</td>
                                    <td>{product.quantity}</td>
                                    <td>
                                        <a href="#" className="btn btn-sm btn-outline-secondary"
                                            onClick={e => del(product.id)}
                                        >
                                            Delete
                                        </a>
                                    </td>
                                </tr>
                            })
                        )}
                    </tbody>
                </table>
            </div>
        </Wrapper>
    );
}