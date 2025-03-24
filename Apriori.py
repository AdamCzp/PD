from itertools import combinations


def get_support(itemset, transactions):
    return sum(1 for transaction in transactions if itemset.issubset(transaction))


def apriori(transactions, min_support):
    items = set(item for transaction in transactions for item in transaction)
    current_itemsets = [{item} for item in items]
    frequent_itemsets = []
    k = 1

    while current_itemsets:
        next_itemsets = []
        for itemset in current_itemsets:
            support = get_support(itemset, transactions) / len(transactions)
            if support >= min_support:
                frequent_itemsets.append((itemset, support))
                for item in items:
                    new_itemset = itemset | {item}
                    if len(new_itemset) == k + 1 and new_itemset not in next_itemsets:
                        next_itemsets.append(new_itemset)
        current_itemsets = next_itemsets
        k += 1

    return frequent_itemsets


def generate_rules(frequent_itemsets, transactions, min_confidence):
    rules = []
    total_transactions = len(transactions)
    support_dict = {frozenset(itemset): support for itemset, support in frequent_itemsets}

    for itemset, support in frequent_itemsets:
        if len(itemset) >= 2:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = set(antecedent)
                    consequent = itemset - antecedent
                    if consequent:
                        antecedent_support = support_dict[frozenset(antecedent)]
                        consequent_support = support_dict[frozenset(consequent)]
                        confidence = support / antecedent_support
                        lift = confidence / consequent_support
                        if confidence >= min_confidence:
                            rules.append((antecedent, consequent, support, confidence, lift))
    return rules


def main():
    transactions = [
        {'Mleko', 'Chleb', 'Masło'},  # ID 1
        {'Mleko', 'Chleb'},  # ID 2
        {'Mleko', 'Masło'},  # ID 3
        {'Chleb', 'Masło'},  # ID 4
        {'Mleko', 'Chleb', 'Masło'}  # ID 5
    ]

    min_support = 0.4  # 40%
    min_confidence = 0.7  # 70%

    print("=== Apriori - Częste Zbiory ===")
    frequent_itemsets = apriori(transactions, min_support)
    for itemset, support in frequent_itemsets:
        print(f"{set(itemset)} - Wsparcie: {support:.2f}")

    print("\n=== Reguły Asocjacyjne (z Confidence i Lift) ===")
    rules = generate_rules(frequent_itemsets, transactions, min_confidence)

    found = False
    for antecedent, consequent, support, confidence, lift in rules:
        rule_str = f"{set(antecedent)} ⇒ {set(consequent)}"
        print(f"{rule_str} | Support: {support:.2f} | Confidence: {confidence:.2f} | Lift: {lift:.2f}")
        # Sprawdź czy to szukana reguła
        if antecedent == {'Mleko', 'Chleb'} and consequent == {'Masło'}:
            found = True

    if not found:
        print("\nReguła {Mleko, Chleb} ⇒ {Masło} nie spełnia minimalnego confidence lub support.")
    else:
        print("\nReguła {Mleko, Chleb} ⇒ {Masło} została znaleziona!")


if __name__ == "__main__":
    main()
