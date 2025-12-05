"""
Utilitaires pour le système de recommandation de produits basé sur la similarité cosinus.
"""
import math
from typing import List, Dict, Tuple


def normalize_value(value, min_val, max_val):
    """
    Normalise une valeur entre 0 et 1.
    
    Args:
        value: La valeur à normaliser
        min_val: Valeur minimale de la plage
        max_val: Valeur maximale de la plage
    
    Returns:
        float: Valeur normalisée entre 0 et 1
    """
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)


def product_vector(product, price_stats: Dict, ram_stats: Dict, storage_stats: Dict) -> List[float]:
    """
    Convertit un produit en vecteur numérique pour le calcul de similarité.
    
    Le vecteur contient :
    - ID de catégorie (normalisé)
    - ID de marque (normalisé)
    - Prix normalisé
    - RAM normalisée
    - Stockage normalisé
    - Taille écran normalisée
    - Système d'exploitation (encodé)
    - Réseau (encodé)
    - État/Condition (encodé)
    
    Args:
        product: Instance du modèle Product
        price_stats: Dict avec 'min' et 'max' des prix
        ram_stats: Dict avec 'min' et 'max' de la RAM
        storage_stats: Dict avec 'min' et 'max' du stockage
    
    Returns:
        List[float]: Vecteur représentant le produit
    """
    vector = []
    
    # 1. Catégorie (poids important - 2x)
    category_id = product.categorie.id if product.categorie else 0
    vector.append(float(category_id))
    vector.append(float(category_id))  # Double poids pour la catégorie
    
    # 2. Marque (poids important - 1.5x)
    brand_id = product.brand.id if product.brand else 0
    vector.append(float(brand_id))
    vector.append(float(brand_id) * 0.5)  # Poids supplémentaire
    
    # 3. Prix normalisé
    price = float(product.price)
    normalized_price = normalize_value(
        price, 
        price_stats.get('min', 0), 
        price_stats.get('max', 1)
    )
    vector.append(normalized_price)
    
    # 4. RAM normalisée
    ram = float(product.ram) if product.ram else 0
    normalized_ram = normalize_value(
        ram,
        ram_stats.get('min', 0),
        ram_stats.get('max', 1)
    )
    vector.append(normalized_ram)
    
    # 5. Stockage normalisé
    storage = float(product.storage) if product.storage else 0
    normalized_storage = normalize_value(
        storage,
        storage_stats.get('min', 0),
        storage_stats.get('max', 1)
    )
    vector.append(normalized_storage)
    
    # 6. Taille écran normalisée
    screen_size = float(product.screen_size) if product.screen_size else 0
    normalized_screen = normalize_value(screen_size, 4.0, 7.0)  # Plage typique des smartphones
    vector.append(normalized_screen)
    
    # 7. Système d'exploitation (encodage one-hot simplifié)
    os_mapping = {'android': 1.0, 'ios': 0.8, 'other': 0.3}
    os_value = os_mapping.get(product.operating_system, 0.5)
    vector.append(os_value)
    
    # 8. Réseau (valeur numérique)
    network_mapping = {'2g': 0.25, '3g': 0.5, '4g': 0.75, '5g': 1.0}
    network_value = network_mapping.get(product.network, 0.5)
    vector.append(network_value)
    
    # 9. Condition/État
    condition_mapping = {'new': 1.0, 'refurbished': 0.7, 'used': 0.4}
    condition_value = condition_mapping.get(product.condition, 0.7)
    vector.append(condition_value)
    
    # 10. Couleur (hash simple pour similarité)
    color_hash = hash(product.color.lower() if product.color else '') % 10 / 10.0
    vector.append(color_hash)
    
    return vector


def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
    """
    Calcule la similarité cosinus entre deux vecteurs.
    
    La similarité cosinus mesure l'angle entre deux vecteurs.
    Valeur entre -1 et 1, où 1 signifie identique, 0 orthogonal, -1 opposé.
    
    Args:
        vector_a: Premier vecteur
        vector_b: Deuxième vecteur
    
    Returns:
        float: Similarité cosinus entre 0 et 1
    """
    if len(vector_a) != len(vector_b):
        raise ValueError("Les vecteurs doivent avoir la même dimension")
    
    # Produit scalaire (dot product)
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    
    # Magnitude (norme) de chaque vecteur
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))
    
    # Éviter la division par zéro
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    # Calcul de la similarité cosinus
    similarity = dot_product / (magnitude_a * magnitude_b)
    
    # Normaliser entre 0 et 1 (au lieu de -1 et 1)
    return (similarity + 1) / 2


def calculate_product_similarities(target_product, all_products) -> List[Tuple[int, float]]:
    """
    Calcule la similarité entre un produit cible et tous les autres produits.
    
    Args:
        target_product: Le produit pour lequel on cherche des recommandations
        all_products: QuerySet de tous les produits (excluant le produit cible)
    
    Returns:
        List[Tuple[int, float]]: Liste de tuples (product_id, similarity_score) triée par score décroissant
    """
    # Calculer les statistiques pour la normalisation
    prices = [float(p.price) for p in all_products if p.price]
    rams = [float(p.ram) for p in all_products if p.ram]
    storages = [float(p.storage) for p in all_products if p.storage]
    
    price_stats = {
        'min': min(prices) if prices else 0,
        'max': max(prices) if prices else 1
    }
    ram_stats = {
        'min': min(rams) if rams else 0,
        'max': max(rams) if rams else 1
    }
    storage_stats = {
        'min': min(storages) if storages else 0,
        'max': max(storages) if storages else 1
    }
    
    # Créer le vecteur du produit cible
    target_vector = product_vector(target_product, price_stats, ram_stats, storage_stats)
    
    # Calculer la similarité avec chaque produit
    similarities = []
    for product in all_products:
        if product.id == target_product.id:
            continue  # Skip le produit lui-même
        
        try:
            product_vec = product_vector(product, price_stats, ram_stats, storage_stats)
            similarity_score = cosine_similarity(target_vector, product_vec)
            
            # Bonus si même catégorie (augmente le score de 20%)
            if product.categorie and target_product.categorie and product.categorie.id == target_product.categorie.id:
                similarity_score = min(1.0, similarity_score * 1.2)
            
            # Bonus si même marque (augmente le score de 15%)
            if product.brand and target_product.brand and product.brand.id == target_product.brand.id:
                similarity_score = min(1.0, similarity_score * 1.15)
            
            similarities.append((product.id, similarity_score))
        except Exception as e:
            # En cas d'erreur, on ignore ce produit
            print(f"Erreur lors du calcul de similarité pour le produit {product.id}: {e}")
            continue
    
    # Trier par score de similarité décroissant
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities


def get_recommended_products(target_product, all_products, limit=10):
    """
    Obtient les produits recommandés pour un produit donné.
    
    Args:
        target_product: Le produit pour lequel on cherche des recommandations
        all_products: QuerySet de tous les produits disponibles
        limit: Nombre maximum de recommandations à retourner (défaut: 10)
    
    Returns:
        List: Liste des produits recommandés triés par pertinence
    """
    # Calculer les similarités
    similarities = calculate_product_similarities(target_product, all_products)
    
    # Récupérer les IDs des produits les plus similaires
    recommended_ids = [prod_id for prod_id, score in similarities[:limit]]
    
    # Récupérer les objets Product dans l'ordre de similarité
    recommended_products = []
    for prod_id in recommended_ids:
        try:
            product = all_products.get(id=prod_id)
            recommended_products.append(product)
        except:
            continue
    
    return recommended_products
