To determine which file is working better, we need to consider the following factors:

Execution Time: How long it takes to perform the recommendation calculation and evaluation.
Precision and Recall: The accuracy of the recommendations as measured by Precision@5 and Recall@5.
Here are the results for each file:

cosine_eval.py Results:
Average Precision@5: 0.1884
Average Recall@5: 0.3405
Time taken for evaluation: 35.57 seconds
rec_eval.py Results:
Average Precision@5: 0.1848
Average Recall@5: 0.3330
Total recommendation calculation time: 4.43 seconds
Total recommendation process time: 4.72 seconds
Analysis:
Execution Time:

rec_eval.py is significantly faster with a total process time of approximately 4.72 seconds.
cosine_eval.py takes much longer with an evaluation time of 35.57 seconds.
Precision and Recall:

cosine_eval.py has slightly better precision (0.1884 vs. 0.1848) and recall (0.3405 vs. 0.3330) compared to rec_eval.py.
Conclusion:
Performance: rec_eval.py performs much faster than cosine_eval.py, completing the recommendation process and evaluation in under 5 seconds.
Accuracy: cosine_eval.py has marginally better precision and recall, but the difference is small.
Given the significant difference in execution time and the marginal difference in precision and recall, rec_eval.py is working better overall for practical purposes, especially in scenarios where speed is critical. If the slight difference in accuracy is acceptable, rec_eval.py provides a much more efficient solution.