import {Wrapper} from "./Wrapper";
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export const Products = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        (async () => {
            try {
                const response = await fetch('http://localhost:8000/products');

                if (!response.ok) {
                    console.error('Failed to fetch products:', response.status);
                    setProducts([]);
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
            }
        })();
    }, []);

    const del = async id => {
        if (window.confirm('Are you sure to delete this record?')) {
            await fetch(`http://localhost:8000/products/${id}`, {
                method: 'DELETE'
            });

            setProducts(products.filter(p => p.id !== id));
        }
    }

    return <Wrapper>
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
                {products.map(product => {
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
                })}
                </tbody>
            </table>
        </div>
    </Wrapper>
}