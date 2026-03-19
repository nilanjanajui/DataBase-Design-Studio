from typing import List, Set, Tuple, FrozenSet

FD = Tuple[FrozenSet[str], FrozenSet[str]]


def is_lossless_decomposition(
    original_attrs: Set[str], decomposed_schemas: List[Set[str]], fds: List[FD]
) -> bool:
    if not original_attrs or not decomposed_schemas or not fds:
        print("Lossless Check Error: Missing inputs")
        return False

    attrs = sorted(original_attrs)
    n = len(decomposed_schemas)

    # ✅ Tableau is a list of rows (one row per decomposed schema)
    # Each row is a dict: attribute → symbol
    # a_j means "distinguished symbol" (this schema contains this attr)
    # b_i_j means "non-distinguished symbol"
    tableau = []
    for i, schema in enumerate(decomposed_schemas):
        row = {}
        for j, attr in enumerate(attrs):
            if attr in schema:
                row[attr] = f"a_{j}"  # distinguished
            else:
                row[attr] = f"b_{i}_{j}"  # non-distinguished
        tableau.append(row)

    print("\nInitial Tableau:")
    for i, row in enumerate(tableau):
        print(f"  Row {i}: {row}")

    # ✅ Apply FDs: if two rows agree on LHS, make them agree on RHS
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            # Check all pairs of rows
            for i in range(n):
                for k in range(n):
                    if i == k:
                        continue

                    # Do rows i and k agree on all LHS attributes?
                    lhs_agree = all(
                        tableau[i].get(attr) == tableau[k].get(attr)
                        for attr in lhs
                        if attr in attrs
                    )

                    if lhs_agree:
                        # Make them agree on RHS — prefer distinguished symbol
                        for attr in rhs:
                            if attr not in attrs:
                                continue
                            si = tableau[i].get(attr)
                            sk = tableau[k].get(attr)
                            if si != sk:
                                # Pick distinguished (a_j) over non-distinguished
                                if si and si.startswith("a_"):
                                    if tableau[k][attr] != si:
                                        tableau[k][attr] = si
                                        changed = True
                                elif sk and sk.startswith("a_"):
                                    if tableau[i][attr] != sk:
                                        tableau[i][attr] = sk
                                        changed = True

    print("\nFinal Tableau:")
    for i, row in enumerate(tableau):
        print(f"  Row {i}: {row}")

    # ✅ Lossless if any row is all distinguished symbols (all a_j)
    distinguished = {attr: f"a_{j}" for j, attr in enumerate(attrs)}
    for i, row in enumerate(tableau):
        if all(row.get(attr) == distinguished[attr] for attr in attrs):
            print(f"\n✅ Lossless confirmed via row {i}")
            return True

    print("\n❌ Lossless check FAILED")
    return False
